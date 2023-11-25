from django.contrib import admin
from django.urls import path , include
from . import views
from django.contrib.auth import views as auth_view
app_name = 'app1'
urlpatterns = [
path('',views.home , name ="home"),
path('list_Recette/',views.list , name="list"),
path('create_recette/',views.create_recette , name ="create_recette"),
path('delet/<int:ID>/',views.delete, name="delete"),
path('update/<path:ID>/',views.update ,name= 'update'),
path('Profile/',views.Profile , name ="Profile"),

path('logup/',views.users, name="logup"), #add referent
path('logoutuser/',views.logoutuser , name="logoutuser"),
path('login/',auth_view.LoginView.as_view(template_name='app1/login.html') , name="login"),
path("password_reset_request/", views.password_reset_request, name="password_reset_request"),
path('reset/<uidb64>/<token>', views.passwordResetConfirm, name='password_reset_confirm'),
]