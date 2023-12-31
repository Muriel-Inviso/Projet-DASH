# Generated by Django 4.2.3 on 2023-07-17 11:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Connexion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_server', models.CharField(max_length=150)),
                ('user_name', models.CharField(max_length=250)),
                ('password', models.CharField(max_length=150)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Societe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, null=True, unique=True, verbose_name='Nom du Société')),
                ('active', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'ordering': ['name', 'active'],
            },
        ),
        migrations.CreateModel(
            name='Tiers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intitule', models.CharField(max_length=150, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='AssociationSociete',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('societe1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='societe1_associations', to='home.societe', verbose_name='Societe 1')),
                ('societe2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='societe2_associations', to='home.societe', verbose_name='Societe 2')),
                ('tiers', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.tiers', verbose_name='Numéro Tiers')),
                ('type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.type', verbose_name='Type de Transaction')),
            ],
        ),
    ]
