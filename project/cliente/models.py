from django.db import models

class Client(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    email = models.EmailField()


class Teacher(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    skill = models.CharField(max_length=30)


class Product(models.Model):
    nombre = models.CharField(max_length=30)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
