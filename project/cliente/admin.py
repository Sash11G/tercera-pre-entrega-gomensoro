from django.contrib import admin
from . import models
# Register your models here.



class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'contenido', 'fecha', 'autor')

class AvatarAdmin(admin.ModelAdmin):
    list_display = ('user', 'imagen')

admin.site.register(models.BlogPost, BlogAdmin)
admin.site.register(models.Avatar, AvatarAdmin)





