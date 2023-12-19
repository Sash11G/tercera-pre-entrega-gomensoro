from django.db import models
from PIL import Image, ImageOps
from django.contrib import admin
from django.contrib.auth.models import User, AbstractUser


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    



class Avatar(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    imagen = models.FileField(upload_to="uploads/avatares", null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.imagen}"
    

    
class BlogPost(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.ForeignKey(Avatar, on_delete=models.SET_NULL, null=True, blank=True)
    categoria = models.ManyToManyField(Category)
    post_image = models.ImageField(upload_to='uploads/posts/', null=True, blank=True)

    def __str__(self):
        return self.titulo