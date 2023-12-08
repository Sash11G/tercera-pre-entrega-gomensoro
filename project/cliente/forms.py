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
        fields = ["nombre", "apellido", "skill"]