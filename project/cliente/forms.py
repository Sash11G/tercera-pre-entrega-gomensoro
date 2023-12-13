from django import forms

from . import models


class ClientForm(forms.ModelForm):
    class Meta:
        model = models.Client
        fields = ["nombre", "apellido", "email"]



class ProductForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = ["nombre", "precio"]


class ProductBuscarFormulario(forms.Form):
    product = forms.CharField()

class TeacherForm(forms.ModelForm):
    class Meta:
        model = models.Teacher
        fields = ["nombre", "apellido", "skill", "foto_perfil"]



## USER LOGIN ETC ##

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User as UserModel    


class UserCreationFormulario(UserCreationForm):
    email = forms.EmailField(label="Email", widget=forms.TextInput)
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat Password", widget=forms.PasswordInput)

    class Meta:
        model = UserModel
        fields = ["username", "password1", "password2", "email"]
        help_texts = {k: "" for k in fields}


class UserEditionFormulario(UserChangeForm):
    email = forms.EmailField()
    first_name = forms.CharField(label="Nombre", widget=forms.PasswordInput)
    last_name = forms.CharField(label="Apellido", widget=forms.PasswordInput)
    password = None

    class Meta:
        model = UserModel
        fields = ["email", "first_name", "last_name"]
        help_texts = {k: "" for k in fields}