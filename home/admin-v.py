from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Connexion, Type, Tiers, Societe, AssociationSociete
from .resources import AssociationSocieteResource

# Register the other models as usual
admin.site.register(Connexion)
admin.site.register(Type)
admin.site.register(Tiers)
admin.site.register(Societe)


# Register the AssociationSociete model using ImportExportModelAdmin
@admin.register(AssociationSociete)
class AssociationSocieteAdmin(ImportExportModelAdmin):
    resource_class = AssociationSocieteResource
    list_display = ('societe1', 'societe2', 'type', 'tiers')
    list_filter = ('type', 'tiers')
    search_fields = ('societe1__name', 'societe2__name')
