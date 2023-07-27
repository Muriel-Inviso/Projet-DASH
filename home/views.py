import pandas as pd
import pyodbc
from django.shortcuts import render, redirect
from .models import Societe, AssociationSociete, Type, Tiers, Connexion, Indentite
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ValidationError
from .forms import ImportExcelForm
from openpyxl import load_workbook

server1 = '192.168.1.161'
server2 = '192.168.1.7'
username = 'reader'
password = 'm1234'


def get_connection_string(server, database):
    conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};" \
               f"DATABASE={database};UID={username};PWD={password}"

    servers_to_try = [server, server2]

    for server_to_try in servers_to_try:
        try:
            with pyodbc.connect(conn_str.replace(server, server_to_try)) as connection:
                # Test the connection to the server by executing a sample query
                with connection.cursor() as cursor:
                    cursor.execute("SELECT 1")
                print(f'Successfully connected to Server: {server_to_try}')
                return conn_str.replace(server, server_to_try)
        except pyodbc.OperationalError as e:
            print(f'Failed to connect to Server: {server_to_try}, Error: {e}')

    # If none of the servers connected successfully, raise an error
    raise ValidationError("Failed to connect to both servers.")


def chercher(database, ct_num, cg_num):
    conn_str = get_connection_string(server1, database)

    # Connexion à la base de données
    try:
        with pyodbc.connect(conn_str) as connection:
            # Création d'un curseur
            cursor = connection.cursor()

            ct_num = format_tuple(ct_num)
            cg_num = format_tuple(cg_num)

            query = "SELECT EC_PIECE, CG_NUM, EC_INTITULE, CASE WHEN EC_SENS =0 THEN EC_MONTANT END AS DEBIT," \
                    f" CASE WHEN EC_SENS =1 THEN EC_MONTANT END AS CREDIT FROM F_ECRITUREC WHERE (CT_NUM in {ct_num}" \
                    f" OR CG_NUM in {cg_num}) AND year(jm_date)=2023"

            print(f'Query : {query}')

            cursor.execute(query)

            # Récupération des résultats
            rows = cursor.fetchall()
            print(rows)
    except pyodbc.OperationalError as e:
        message = f"Une erreur s'est produite lors de la connexion à la base de données INVISO : {e}"
        raise ValidationError(message)

    # Liste pour stocker les résultats
    data = []

    for row in rows:
        EC_PIECE, CG_NUM, EC_INTITULE, DEBIT, CREDIT = row

        item = {
            'ec_piece': EC_PIECE,
            'cg_num': str(CG_NUM)[:5],
            'ec_intitule': EC_INTITULE,
            'debit': "{:.2f}".format(float(DEBIT)) if DEBIT else '',
            'credit': "{:.2f}".format(float(CREDIT)) if CREDIT else ''
        }

        data.append(item)

    return data


def format_tuple(t):
    if len(t) == 1:
        return "('{}')".format(t[0])  # Ajoute des guillemets simples et supprime la virgule
    return "({})".format(', '.join("'{}'".format(value) for value in t))


def inter_value(value):
    ct_num = []  # Utiliser un tuple vide au lieu d'une chaîne de caractères
    cg_num = []  # Utiliser un tuple vide au lieu d'une chaîne de caractères
    for ass in value:
        if ass.type.intitule == 'CT':
            ct_num.append(ass.tiers.value)  # Utiliser une virgule pour créer un tuple avec une seule valeur
        else:
            cg_num.append(ass.tiers.value)  # Utiliser une virgule pour créer un tuple avec une seule valeur

    # Créer une liste de tuples avec les tuples contenant une seule valeur
    result = [tuple(ct_num), tuple(cg_num)]
    print(f'R : {result} ct_num : {ct_num} et cg_num: {cg_num}')
    return result


def identification(societe):
    pass


def index(request):
    results1 = []
    results2 = []
    message = None

    associations1 = {}
    associations2 = {}

    societe_1_name = ''
    societe_2_name = ''

    # Vérifier si l'utilisateur est connecté
    # if not request.session.get('user_session', False):
    #     # Si l'utilisateur n'est pas connecté, redirigez-le vers la page de connexion.
    #     return redirect('auth:login')

    if request.method == 'POST':
        form = ImportExcelForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['excel_file']
            try:
                importer_associations(file)
                message = 'Importation réussie !'
                return redirect('home:index')
            except ValidationError as e:
                message = f"Une erreur s'est produite lors du traitement du fichier excel : {str(e)}"
            except Exception as e:
                message = f"Une erreur s'est produite lors du traitement du fichier excel : {str(e)}"
        else:
            message = 'Formulaire invalide, veuillez vérifier les champs !'
    else:
        form = ImportExcelForm()
        societe_1_name = request.GET.get('societe_1_name', '')
        societe_2_name = request.GET.get('societe_2_name', '')

        if societe_1_name and societe_2_name and societe_1_name != societe_2_name:
            associations1 = AssociationSociete.objects.filter(
                societe1__name__exact=societe_1_name,
                societe2__name__exact=societe_2_name,
            )

            associations2 = AssociationSociete.objects.filter(
                societe1__name__exact=societe_2_name,
                societe2__name__exact=societe_1_name,
            )

            value1 = inter_value(associations1)
            value2 = inter_value(associations2)

            print("-------------------------------------------------")
            print(f'value A : (1) : {value1[0]}, (2) :{value1[1]}')
            print(f'value B : (1) : {value2[0]}, (2) :{value2[1]}')
            print("-------------------------------------------------")
            print("")
            if not value1[0]:
                value1[0] = ('',)
            if not value1[1]:
                value1[1] = ('',)
            if not value2[0]:
                value2[0] = ('',)
            if not value2[1]:
                value2[1] = ('',)

            try:
                results1 = chercher(database=societe_1_name, ct_num=value1[0], cg_num=value1[1])
                results2 = chercher(database=societe_2_name, ct_num=value2[0], cg_num=value2[1])
            except Exception as e:
                message = f"Une erreur s'est produite lors de la recherche dans la base de données :  {str(e)}"

        else:
            associations1 = {}
            associations2 = {}
        # value_tiers = tuple(inter_value(associations1) + inter_value(associations2))

    societe = Societe.objects.filter(active=True)

    context = {
        'associations1': associations1,
        'associations2': associations2,
        'results1': results1,
        'results2': results2,
        'societes': societe,
        'societe_1_name': societe_1_name,
        'societe_2_name': societe_2_name,
        'form': form,
        'message': message
    }
    return render(request, 'home/index.html', context)


def import_data(request):
    if request.method == 'POST':
        form = ImportExcelForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['excel_file']
            try:
                importer_associations(file)
                success_message = 'Importation réussie !'
                return JsonResponse({'success_message': success_message})
            except ValidationError as e:
                error_message = str(e)
                return JsonResponse({'error_message': error_message})
    else:
        form = ImportExcelForm()
    return JsonResponse({'form': form})


def identite_check(value):
    value = str(value).strip()
    try:
        identite_obj = Indentite.objects.filter(name__exact=value).first()
        return identite_obj.correspondance if identite_obj else value
    except Indentite.DoesNotExist:
        return value


def importer_associations(file):
    wb = load_workbook(file)
    sheets = wb.sheetnames

    for sheet_name in sheets:
        df = pd.read_excel(file, sheet_name=sheet_name)
        required_columns = ['SOCIETE1', 'TIERS', 'SOCIETE2', 'TYPE']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValidationError(
                f"Les colonnes suivantes sont manquantes dans la feuille '{sheet_name}': {', '.join(missing_columns)}")

        for index, row in df.iterrows():
            societe1_name = row['SOCIETE1']
            tiers_value = row['TIERS']
            societe2_name = row['SOCIETE2']
            type_intitule = row['TYPE']

            societe1, _ = Societe.objects.get_or_create(name=identite_check(societe1_name))
            societe2, _ = Societe.objects.get_or_create(name=identite_check(societe2_name))
            tiers, _ = Tiers.objects.get_or_create(value=str(tiers_value).strip())
            type_obj, _ = Type.objects.get_or_create(intitule=str(type_intitule).strip())

            AssociationSociete.objects.get_or_create(
                societe1=societe1,
                societe2=societe2,
                tiers=tiers,
                type=type_obj,
                # connexion=connexion  # Associer la connexion à la société
            )
