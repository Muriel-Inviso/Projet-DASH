# Generated by Django 4.2.3 on 2023-08-01 11:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_tableau_intercohistorique'),
    ]

    operations = [
        migrations.AlterField(
            model_name='intercohistorique',
            name='tableau1',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='historique_tableau1', to='home.tableau'),
        ),
        migrations.AlterField(
            model_name='intercohistorique',
            name='tableau2',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='historique_tableau2', to='home.tableau'),
        ),
    ]