from django.contrib import admin
from . import models
# Register your models here.

class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'apellido', 'email', )

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'precio')

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'apellido', 'skill')

admin.site.register(models.Client, ClientAdmin)
admin.site.register(models.Teacher, TeacherAdmin)
admin.site.register(models.Product, ProductAdmin)

