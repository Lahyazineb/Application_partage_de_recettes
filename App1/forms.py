from django import forms
from .models import * # imort all the models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm, PasswordResetForm
from django_recaptcha.fields import ReCaptchaField 
class RecetteForm(forms.ModelForm):
    class Meta:
        model = Recette
        fields = ['nom', 'ingredients', 'etapes_preparation', 'duree_preparation', 'photo']

    # You can add additional customization to the form fields if needed
    nom = forms.CharField(label='Nom de la recette', max_length=255)
    ingredients = forms.CharField(label='Liste des ingrédients nécessaires pour la recette', widget=forms.Textarea)
    etapes_preparation = forms.CharField(label='Les étapes à suivre pour créer la recette', widget=forms.Textarea)
    duree_preparation = forms.IntegerField(label='Temps de préparation')
    photo = forms.ImageField(label='Photo optionnelle', required=False)

# pour ce conecter 
class logupform(UserCreationForm):
    email = forms.EmailField(help_text='A valid email address, please.', required=True)
    first_name= forms.CharField(label='Prénom ', max_length=600)
    last_name= forms.CharField(label='Nom de famille ', max_length=600)
    username = forms.ChoiceField(label="Nom d'utilisateur" )
    password1 = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmer le mot de passe', widget=forms.PasswordInput)
    class Meta:
        model= User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2' ]
# for setting the password 
class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']
# cette class c'est pour recuper le mot de pass 
class ResetPasswordForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)

    captcha = ReCaptchaField()
