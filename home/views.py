import pandas as pd
import pyodbc
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Societe, AssociationSociete, Type, Tiers, Connexion
from django.http import JsonResponse
from django.db import OperationalError
from django.core.exceptions import ValidationError
from .forms import ImportExcelForm
from openpyxl import load_workbook

server = '192.168.1.161'
username = 'reader'
password = 'm1234'


def chercher(database, ct_num, cg_num):
    # database = str(base)
    #
    # print(f'ct_num inter : {ct_num}')
    # print(f'cg_num inter : {cg_num}')

    # Chaîne de connexion
    conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"
    # Connexion à la base de données
    try:
        with pyodbc.connect(conn_str) as connection:
            # Création d'un curseur
            cursor = connection.cursor()

            # if database == 'FLY TECHNOLOGIES':
            #     value = ('C22013', 'F00057')
            #
            # elif database == 'IDMOTORS':
            #     ct_num = ('C22272', 'F22725')
            #     cg_num = ('C22272', 'F22725')

            # Exécution d'une requête SELECT
            # query = "SELECT EC_PIECE, CG_NUM, EC_INTITULE, CASE WHEN EC_SENS =0 THEN EC_MONTANT END AS DEBIT," \
            #         f" CASE WHEN EC_SENS =1 THEN EC_MONTANT END AS CREDIT FROM F_ECRITUREC WHERE (CT_NUM in {value} OR CG_NUM in {value2}) " \
            #         "AND year(jm_date)=2023"
            if ct_num == ():
                ct_num = cg_num
            elif cg_num == ():
                cg_num = ct_num
            #
            # print(f'ct_num use : {ct_num}')
            # print(f'cg_num use : {cg_num}')

            query = "SELECT EC_PIECE, CG_NUM, EC_INTITULE, CASE WHEN EC_SENS =0 THEN EC_MONTANT END AS DEBIT," \
                    f" CASE WHEN EC_SENS =1 THEN EC_MONTANT END AS CREDIT FROM F_ECRITUREC WHERE (CT_NUM in {ct_num} " \
                    f"OR CG_NUM in {cg_num}) AND year(jm_date)=2023"

            cursor.execute(query)

            # Récupération des résultats
            rows = cursor.fetchall()
            # print(rows)
    except OperationalError as e:
        message = "Une erreur s'est produit lors de la connexion à la base de donnée INVISO"
        print(str(e))
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


def inter_value(value):
    ct_num = []
    cg_num = []
    for ass in value:
        if ass.type.intitule == 'CT':
            ct_num.append(ass.tiers.value)
        else:
            cg_num.append(ass.tiers.value)
    result = [tuple(ct_num), tuple(cg_num)]
    print(f'R : {result}')
    return result


# @login_required
def index(request):
    results1 = []
    results2 = []
    message = None
    if request.session.get('user_session', True):
        bases = Societe.objects.filter(active=True)

        if request.method == 'POST':
            form = ImportExcelForm(request.POST, request.FILES)
            if form.is_valid():
                file = request.FILES['excel_file']
                try:
                    importer_associations(file)
                    message = 'Importation réussie !'
                    return redirect('home:index')
                except ValidationError as e:
                    message = f"Une erreur s'est produit lors du traitement de fichier excel : {str(e)}"
                except Exception as e:
                    message = f"Une erreur s'est produit lors du traitement de fichier excel : {str(e)}"
            else:
                message = 'Formulaire invalide, veuillez verifier les champs !'
        else:
            form = ImportExcelForm()
            societe_1_name = request.GET.get('societe_1_name', '')
            societe_2_name = request.GET.get('societe_2_name', '')

            if societe_1_name != societe_2_name:
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
                try:
                    results1 = chercher(database=societe_1_name, ct_num=value1[0], cg_num=value1[1])
                    results2 = chercher(database=societe_2_name, ct_num=value2[0], cg_num=value2[1])
                except Exception as e:
                    message = f" Une erreur s'est produit lors de recherche dans la base de donnee :  {str(e)}"

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
    else:
        return redirect('auth:login')


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

            societe1, _ = Societe.objects.get_or_create(name=str(societe1_name).strip())
            societe2, _ = Societe.objects.get_or_create(name=str(societe2_name).strip())
            tiers, _ = Tiers.objects.get_or_create(value=str(tiers_value).strip())
            type_obj, _ = Type.objects.get_or_create(intitule=str(type_intitule).strip())

            AssociationSociete.objects.get_or_create(
                societe1=societe1,
                societe2=societe2,
                tiers=tiers,
                type=type_obj,
                # connexion=connexion  # Associer la connexion à la société
            )
