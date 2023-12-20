from django import forms
from . import models
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User as UserModel   
from PIL import Image, ImageOps




class BlogPostForm(forms.ModelForm):
    # Define the choices for the 'categoria' field
    CATEGORIES_CHOICES = [
        ('fitness', 'Fitness'),
        ('nutrition', 'Nutrition'),
        ('mental_health', 'Mental Health'),
        ('wellness_tips', 'Wellness Tips'),
        ('mindfulness', 'Mindfulness'),
        ('recipes', 'Healthy Recipes'),
        # Add more choices as needed
    ]

    categoria = forms.ChoiceField(choices=CATEGORIES_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = models.BlogPost
        fields = ['titulo', 'contenido', 'categoria', 'post_image']

