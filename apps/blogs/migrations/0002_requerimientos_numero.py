# Generated by Django 4.2.3 on 2023-07-09 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='requerimientos',
            name='numero',
            field=models.IntegerField(default=0, verbose_name='Numero de requerimiento'),
            preserve_default=False,
        ),
    ]
