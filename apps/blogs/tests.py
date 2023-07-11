# python manage.py test apps.blogs
from config.wsgi import *
from apps.blogs.models import Requerimientos

for i in Requerimientos.objects.all():
    print(f'Requerimiento: {i.nombre}')
