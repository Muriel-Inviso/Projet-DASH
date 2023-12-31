# Generated by Django 4.2.3 on 2023-07-17 11:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='associationsociete',
            name='societe1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='societe1_associations', to='home.societe', verbose_name='Societe 1'),
        ),
        migrations.AlterField(
            model_name='associationsociete',
            name='societe2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='societe2_associations', to='home.societe', verbose_name='Societe 2'),
        ),
    ]
