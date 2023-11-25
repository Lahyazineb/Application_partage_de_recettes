# Generated by Django 4.2.7 on 2023-11-25 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Recette',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=255, verbose_name='Nom de la recette')),
                ('ingredients', models.TextField(verbose_name='Liste des ingrédients nécessaires pour la recette')),
                ('etapes_preparation', models.TextField(verbose_name='les étapes a suivre pour crée la recette')),
                ('duree_preparation', models.IntegerField(verbose_name='Temps de preparation')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='photos/')),
            ],
        ),
    ]