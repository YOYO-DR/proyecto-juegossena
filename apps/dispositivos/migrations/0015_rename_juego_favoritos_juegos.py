# Generated by Django 4.2.1 on 2023-09-05 23:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dispositivos', '0014_juegos_sistemaoperativo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='favoritos',
            old_name='juego',
            new_name='juegos',
        ),
    ]
