from import_export import resources
from .models import AssociationSociete, Societe, Type, Tiers


class AssociationSocieteResource(resources.ModelResource):
    class Meta:
        model = AssociationSociete
        import_id_fields = ('societe1__name', 'societe2__name', 'type__intitule', 'tiers__value',)
        skip_unchanged = True
        report_skipped = True

    def before_import_row(self, row, **kwargs):
        # Map the societe names to the corresponding objects for foreign keys
        societe1_name = row['societe1']
        societe2_name = row['societe2']
        type_intitule = row['type']
        tiers_value = row['tiers']

        try:
            row['societe1'] = Societe.objects.get(name=societe1_name)
        except Societe.DoesNotExist:
            row['societe1'] = Societe.objects.create(name=societe1_name, active=False)

        try:
            row['societe2'] = Societe.objects.get(name=societe2_name)
        except Societe.DoesNotExist:
            row['societe2'] = Societe.objects.create(name=societe2_name, active=False)

        try:
            row['type'] = Type.objects.get(intitule=type_intitule)
        except Type.DoesNotExist:
            row['type'] = Type.objects.create(intitule=type_intitule)

        try:
            row['tiers'] = Tiers.objects.get(value=tiers_value)
        except Tiers.DoesNotExist:
            row['tiers'] = Tiers.objects.create(value=tiers_value)
