from django.contrib import admin
from .models import Societe, Connexion, Type, Tiers, AssociationSociete


class AssociationSocieteInline(admin.TabularInline):
    model = AssociationSociete
    fk_name = 'societe1'
    extra = 1


@admin.register(Societe)
class SocieteModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'active', 'created_at', 'updated_at']
    list_filter = ['active']
    search_fields = ['societe1']
    fieldsets = (
        ('Informations générales', {
            'fields': ('name', 'active', 'created_at', 'updated_at')
        }),
        ('Connexion', {
            'fields': ('connexion',),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
    inlines = [AssociationSocieteInline]


@admin.register(Connexion)
class ConnexionModelAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'ip_server', 'active']
    list_filter = ['active']
    search_fields = ['user_name']


@admin.register(Type)
class TypeModelAdmin(admin.ModelAdmin):
    list_display = ['intitule']


@admin.register(Tiers)
class TiersModelAdmin(admin.ModelAdmin):
    list_display = ['value']


@admin.register(AssociationSociete)
class AssociationSocieteModelAdmin(admin.ModelAdmin):
    list_display = ['societe1', 'societe2', 'type', 'tiers']
    list_filter = ['type', 'tiers']
    search_fields = ['societe1__societe1', 'societe2__societe1']