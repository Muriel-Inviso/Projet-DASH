# import pandas as pd
# from django.shortcuts import render
# from django.http import HttpResponse
# from .models import Societe, AssociationSociete, Type, Tiers
# from import_export.formats import base_formats
# from import_export import resources, fields
# from import_export.admin import ImportExportModelAdmin
# from import_export.widgets import ForeignKeyWidget
#
#
# class AssociationSocieteResource(resources.ModelResource):
#     id = fields.Field(attribute='id', column_name='ID')
#
#     class Meta:
#         model = AssociationSociete
#         fields = ('id', 'societe1__name', 'societe2__name', 'tiers__value', 'type__intitule')
#         import_id_fields = ['id']
#
#     societe1__name = fields.Field(
#         column_name='S1',
#         attribute='societe1',
#         widget=ForeignKeyWidget(Societe, 'name')
#     )
#
#     societe2__name = fields.Field(
#         column_name='S2',
#         attribute='societe2',
#         widget=ForeignKeyWidget(Societe, 'name')
#     )
#
#     tiers__value = fields.Field(
#         column_name='TS',
#         attribute='tiers',
#         widget=ForeignKeyWidget(Tiers, 'value')
#     )
#
#     type__intitule = fields.Field(
#         column_name='TP',
#         attribute='type',
#         widget=ForeignKeyWidget(Type, 'intitule')
#     )
#
#
# class AssociationSocieteAdmin(ImportExportModelAdmin):
#     resource_class = AssociationSocieteResource
#     formats = [base_formats.XLSX, base_formats.XLS, base_formats.CSV]
#
#
# def import_data(request):
#     if request.method == 'POST' and request.FILES['file']:
#         file = request.FILES['file']
#         data = pd.read_excel(file)
#         resource = AssociationSocieteResource()
#         dataset = resource.export(data)
#         imported_data = dataset.dict
#
#         for row in imported_data:
#             # Vérifiez si la ligne existe déjà pour éviter les doublons
#             if not AssociationSociete.objects.filter(
#                     societe1__name=row['S1'],
#                     societe2__name=row['S2'],
#                     tiers__value=row['TS'],
#                     type__intitule=row['TP']
#             ).exists():
#                 resource.import_row(row)
#
#         return HttpResponse('Données importées avec succès!')
#     else:
#         return render(request, 'home/import_data.html')
