# Generated by Django 5.0 on 2023-12-21 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='subtitulo',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]