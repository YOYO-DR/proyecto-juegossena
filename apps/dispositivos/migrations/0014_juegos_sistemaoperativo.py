# Generated by Django 4.2.1 on 2023-09-05 19:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dispositivos', '0013_alter_juegos_imagen_imagenesjuego'),
    ]

    operations = [
        migrations.AddField(
            model_name='juegos',
            name='sistemaOperativo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dispositivos.sistemasoperativos', verbose_name='Sistema operativo'),
        ),
    ]
