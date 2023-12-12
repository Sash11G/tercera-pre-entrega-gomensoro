from django.db import models
from PIL import Image, ImageOps

class Client(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    email = models.EmailField()


class Teacher(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    skill = models.CharField(max_length=30)
    foto_perfil = models.ImageField(upload_to='uploads/', null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.foto_perfil:
            max_size = (100, 100)  # Set your desired width and height
            img = Image.open(self.foto_perfil.path)

            # Resize and maintain aspect ratio using ImageOps
            img.thumbnail(max_size)
            img = ImageOps.exif_transpose(img)

            img.save(self.foto_perfil.path)


class Product(models.Model):
    nombre = models.CharField(max_length=30)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
