# Generated by Django 5.0 on 2023-12-12 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0002_rename_producto_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='foto_perfil',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/'),
        ),
    ]