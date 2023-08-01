from django.db import models


class Connexion(models.Model):
    ip_server = models.CharField(max_length=150)
    user_name = models.CharField(max_length=250)
    password = models.CharField(max_length=150)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_name


class Type(models.Model):
    intitule = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.intitule


class Tiers(models.Model):
    value = models.CharField(max_length=150)

    def __str__(self):
        return self.value


class Societe(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Nom du Société', null=True)
    user = models.CharField(max_length=150, default='reader', null=True)
    password = models.CharField(max_length=150, default='m1234', null=True)
    server = models.CharField(max_length=25, default='192.168.1.161', null=True)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', 'active']


class AssociationSociete(models.Model):
    societe1 = models.ForeignKey(Societe, on_delete=models.CASCADE, verbose_name='Societe 1',
                                 related_name='societe1_associations', null=True)
    societe2 = models.ForeignKey(Societe, on_delete=models.CASCADE, verbose_name='Societe 2',
                                 related_name='societe2_associations', null=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Type de Transaction')
    tiers = models.ForeignKey(Tiers, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Numéro Tiers')

    def __str__(self):
        return f"{self.societe1.name} - {self.societe2.name}"


class Indentite(models.Model):
    name = models.CharField(max_length=250)
    correspondance = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Tableau(models.Model):
    base = models.CharField(max_length=50, null=True)
    ecPiece = models.IntegerField()
    ecRefPiece = models.CharField(max_length=50)
    ecNo = models.IntegerField()

    def __str__(self):
        return self.base


class IntercoHistorique(models.Model):
    interco = models.CharField(max_length=10, null=True)
    tableau1 = models.ForeignKey(
        Tableau,
        on_delete=models.CASCADE,
        related_name='historique_tableau1',  # Spécifiez un nom de related_name distinct pour cette clé étrangère
        null=True
    )

    tableau2 = models.ForeignKey(
        Tableau,
        on_delete=models.CASCADE,
        related_name='historique_tableau2',  # Spécifiez un nom de related_name distinct pour cette clé étrangère
        null=True
    )

    def __str__(self):
        return self.interco

    @classmethod
    def get_last_interco(cls):
        last_interco_obj = cls.objects.order_by('-id').first()
        return last_interco_obj.interco if last_interco_obj else None
