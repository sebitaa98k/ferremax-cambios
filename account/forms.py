from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100, label='Nombre de usuario')
    email = forms.EmailField(label='Correo electrónico')
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
    passwordrepetir = forms.CharField(widget=forms.PasswordInput, label='Confirmar contraseña')



class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label='Nombre de usuario')
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')