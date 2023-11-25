
# Create your models here.
from django.db import models

class Recette(models.Model):
    # Id unique de la recette
    ID = models.AutoField(primary_key=True)
    # Nom de la recette
    nom = models.CharField(max_length=255 , verbose_name='Nom de la recette')
    # Liste d'ingrédients (peut être stockée sous forme de texte)
    ingredients = models.TextField(verbose_name='Liste des ingrédients nécessaires pour la recette')
    # Étapes de préparation (peut être stockées sous forme de texte)
    etapes_preparation = models.TextField(verbose_name='les étapes a suivre pour crée la recette')
    # Durée de préparation (en minutes, par exemple)
    duree_preparation = models.IntegerField(verbose_name='Temps de preparation')
    # Photo optionnelle
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)