from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from .models import *  # Update this line with the correct model names and import paths
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout ,get_user_model
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout ,get_user_model#THIS import allows us to use the logut and in fucntion from django 
from django.contrib import messages
from django.db.models.query_utils import Q
from .decorators import  user_not_authenticated
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.db.models.query_utils import Q
from .tokens import account_activation_token
from smtplib import SMTPException
from rest_framework.decorators import api_view
# import shapefileimport
import os.path

from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, 'app1/index.html' )


def login(request):
    if request.method == 'POST':
            username= request.POST.get('username')
            password= request.POST.get('password')
            user = authenticate(request, username=username , password=password)
            if user is not None:
                login(request, user)
                return redirect('app1:Profile')
                
            else :
                
                messages.info(request , "Le nom d'utilisateur ou le mot de passe est incorrect")
                return redirect('app1:loginp')
        
    return render(request, 'app1/Profile.html' )

def logoutuser(request):
    logout(request)
    return redirect('app1:home')

@user_not_authenticated
def password_reset_request(request):
    # Handle POST request for password reset form submission
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)  # Create form instance with POST data
        if form.is_valid():  # Check if form data is valid
            user_email = form.cleaned_data['email']  # Get the email from the form
            associated_user = User.objects.filter(Q(email=user_email)).first()  # Get the user associated with the email
            if associated_user:
                # Generate the password reset email
                subject = "Password Reset request"
                message = render_to_string("App1/mail.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http',
                })
                email = EmailMessage(subject, message, to=[associated_user.email])  # Create an email message
                try:
                    email.send()  # Send the email
                    messages.success(request, "Envoi du mail de réinitialisation du mot de passe")
                except SMTPException as e:
                    messages.error(request, f"Problème d'envoi de l'e-mail de réinitialisation du mot de passe: {str(e)}")
            return redirect('app1:home')  # Redirect after successful form submission

        # Handle form validation errors
        for key, error in list(form.errors.items()):
            if key == 'captcha' and error[0] == 'This field is required.':
                messages.error(request, "Vous devez passer le test CAPTCHA")
                continue
    
    # Handle GET request or invalid form data
    form = ResetPasswordForm()  # Create a new instance of the password reset form
    return render(
        request, 
        "app1/password_reset_request.html", 
        {"form": form}  # Pass the form instance to the template for rendering
    )

def passwordResetConfirm(request, uidb64, token):
    User = get_user_model()

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Votre mot de passe a été modifié. Vous pouvez maintenant vous connecter")
                return redirect('app1:home')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = SetPasswordForm(user)
        return render(request, 'app1/passwordResetConfirm.html', {'form': form}) # where we have the password form 
    else:
        messages.error(request, "Le lien est expiré")

    messages.error(request, 'Quelque chose a mal tourné')
    return redirect("app1:home")

def Profile(request):
    return render(request, 'app1/Profile.html')
def users(request):
    if request.method == 'POST':
        form = logupform(request.POST)
        if form.is_valid():
            form.save()
            # Assuming 'referent' group exists
            username = form.cleaned_data.get('username')
            messages.success(request, f'Bonjour le compte de {username} a été créé avec succès')
           
            return redirect('app1:users')  # Redirect to the 'users' view after successful form submission
    else:
        form = logupform()
    user_list = User.objects.all()
    context = {'form': form, 'user_list': user_list}  # Removed 'message' from context as it's not used
    return render(request, 'app1/logup.html', context)
def list(request):
# query = request.POST.get('q', '')  # Get the value of the 'q' parameter from the URL query string
    listREC =Recette.objects.all()
    context = {'list': listREC,}
    print(listREC,'""""""""""""""""""""""""""""""""')
    return render(request, 'App1/listREC.html', context)

def create_recette(request):
    if request.method == 'POST':
        
        form = RecetteForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the form data to the database
            form.save()
            messages.success(request, "Une nouvelle Recettz a été ajoutée avec succès.", extra_tags='success')
            return render(request, 'App1/form.html', {'form': form})
    else:
        form = RecetteForm()

    return render(request, 'App1/form.html', {'form': form})

def delete(request, ID):
    lot = Recette.objects.get(ID=ID)
    if request.method == 'POST':
        if request.POST['confirm'] == "1":
            lot.delete()
            messages.success(request, 'Objet supprimé avec succès !')
        return redirect('app1:list')
    return render(request , "App1/delete.html",{'ID' : ID})

def update(request, ID=0):
    # Check if the object with the given ID exists
    if ID != 0:
        
        lot = Recette.objects.get(pk=ID)
        print("Id exists" ,lot)
    else:
        lot = None  # No object with ID 0

    if request.method == 'POST':
        formM = RecetteForm(request.POST, instance=lot)  # Bind the form to the submitted data

        if formM.is_valid():
            # Save the form data and update the object if it exists
            formM.save()
            return redirect('app1:list')  # Redirect to the list view (adjust the URL name as needed)
    else:
        # GET request or invalid form submission
        formM = RecetteForm(instance=lot)  # Render the form with the existing object if it exists

    # Render the form template with the form object
    return render(request, 'App1/mod.html', {'formM': formM })
