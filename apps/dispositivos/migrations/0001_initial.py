# Generated by Django 4.2.1 on 2023-08-15 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dispositivos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('espacioGb', models.IntegerField(blank=True, null=True, verbose_name='Espacio gb')),
                ('nombre', models.CharField(blank=True, max_length=200, null=True, verbose_name='Nombre')),
                ('json', models.JSONField(blank=True, null=True, verbose_name='Json presentación')),
            ],
            options={
                'verbose_name': 'Dispositivo',
                'verbose_name_plural': 'Dispositivos',
            },
        ),
        migrations.CreateModel(
            name='Favoritos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Favorito',
                'verbose_name_plural': 'Favoritos',
            },
        ),
        migrations.CreateModel(
            name='Favoritos_UrlJuegos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Favorito_juego',
                'verbose_name_plural': 'Favoritos_juegos',
            },
        ),
        migrations.CreateModel(
            name='Graficas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('nucleos', models.IntegerField(blank=True, null=True, verbose_name='Nucleos')),
            ],
            options={
                'verbose_name': 'Grafica',
                'verbose_name_plural': 'Graficas',
            },
        ),
        migrations.CreateModel(
            name='GraficasGb',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gb', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Espacio gb')),
            ],
            options={
                'verbose_name': 'Grafica gb',
                'verbose_name_plural': 'Graficas gb',
            },
        ),
        migrations.CreateModel(
            name='GraficasVelocidades',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('velocidadMhz', models.IntegerField(verbose_name='Velocidad mhz')),
            ],
            options={
                'verbose_name': 'Grafica velocidad',
                'verbose_name_plural': 'Graficas velocidades',
            },
        ),
        migrations.CreateModel(
            name='Historiales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('busqueda', models.CharField(max_length=100, verbose_name='Busqueda')),
                ('fechaBusqueda', models.DateField(auto_now_add=True, verbose_name='Fecha de busqueda')),
            ],
            options={
                'verbose_name': 'Historial',
                'verbose_name_plural': 'Historiales',
            },
        ),
        migrations.CreateModel(
            name='Juegos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200, unique=True, verbose_name='Nombre')),
                ('urlPagina', models.URLField(verbose_name='Url pagina')),
                ('espacio', models.IntegerField(verbose_name='Espacio necesario')),
            ],
        ),
        migrations.CreateModel(
            name='Procesadores',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('nucleos', models.IntegerField(blank=True, null=True, verbose_name='Nucleos')),
                ('hilos', models.IntegerField(blank=True, null=True, verbose_name='Hilos')),
                ('mhz', models.IntegerField(blank=True, null=True, verbose_name='Potencia Mhz')),
            ],
            options={
                'verbose_name': 'Procesador',
                'verbose_name_plural': 'Procesadores',
            },
        ),
        migrations.CreateModel(
            name='Rams',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gb', models.IntegerField(verbose_name='Espacio gb')),
            ],
            options={
                'verbose_name': 'Ram',
                'verbose_name_plural': 'Rams',
            },
        ),
        migrations.CreateModel(
            name='RamsVelocidades',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('velocidadMhz', models.IntegerField(verbose_name='Velocidad Mhz')),
            ],
            options={
                'verbose_name': 'Ram Velocidad',
                'verbose_name_plural': 'Rams Velocidades',
            },
        ),
        migrations.CreateModel(
            name='SistemasOperativos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True, verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'Sistema Operativo',
                'verbose_name_plural': 'Sistema Operativos',
            },
        ),
        migrations.CreateModel(
            name='Telefonos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numeroTelefono', models.CharField(max_length=20, verbose_name='Numero de telefono')),
            ],
            options={
                'verbose_name': 'Telefono',
                'verbose_name_plural': 'Telefonos',
            },
        ),
        migrations.CreateModel(
            name='TipoRam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=10, verbose_name='Tipo ram')),
            ],
            options={
                'verbose_name': 'Tipo ram',
                'verbose_name_plural': 'Tipos rams',
            },
        ),
    ]
