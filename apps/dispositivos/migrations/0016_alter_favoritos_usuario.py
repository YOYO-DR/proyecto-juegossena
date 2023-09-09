# Generated by Django 4.2.1 on 2023-09-06 02:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dispositivos', '0015_rename_juego_favoritos_juegos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favoritos',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique=True, verbose_name='Usuario'),
        ),
    ]