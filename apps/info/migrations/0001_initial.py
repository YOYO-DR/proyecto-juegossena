# Generated by Django 4.2.1 on 2023-10-13 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PreguntaAyuda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pregunta', models.CharField(max_length=200, unique=True, verbose_name='Pregunta')),
                ('respuesta', models.TextField(verbose_name='Respuesta')),
            ],
            options={
                'verbose_name': 'Pregunta ayuda',
                'verbose_name_plural': 'Preguntas ayuda',
            },
        ),
    ]