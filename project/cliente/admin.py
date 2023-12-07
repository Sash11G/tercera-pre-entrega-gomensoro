from django.contrib import admin
from . import models
# Register your models here.

class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'apellido', 'email', )

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'precio')

admin.site.register(models.Client, ClientAdmin)
admin.site.register(models.Teacher)
admin.site.register(models.Product, ProductAdmin)

