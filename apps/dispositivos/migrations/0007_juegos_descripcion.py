# Generated by Django 4.2.1 on 2023-08-31 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dispositivos', '0006_juegos_imagen'),
    ]

    operations = [
        migrations.AddField(
            model_name='juegos',
            name='descripcion',
            field=models.CharField(default='holi', max_length=300, verbose_name='Descripción'),
            preserve_default=False,
        ),
    ]
