# Generated by Django 4.2.1 on 2023-08-30 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dispositivos', '0003_alter_juegos_espacio'),
    ]

    operations = [
        migrations.AddField(
            model_name='favoritos',
            name='juego',
            field=models.ManyToManyField(to='dispositivos.juegos'),
        ),
        migrations.DeleteModel(
            name='Favoritos_UrlJuegos',
        ),
    ]