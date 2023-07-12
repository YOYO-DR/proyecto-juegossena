import os
from django.db import models

from config.settings import MEDIA_URL, STATIC_URL

class Requerimientos(models.Model):
    numero=models.IntegerField(verbose_name="Numero de requerimiento")
    imagen=models.ImageField(upload_to=f'{MEDIA_URL}blogs/requerimientos/%Y/%m/' if 'WEBSITE_HOSTNAME' in os.environ else 'blogs/requerimientos/%Y/%m/',null=True,blank=True, verbose_name='Mockup requerimiento')
    nombre=models.CharField(max_length=100,null=False,blank=False,verbose_name="Nombre requerimiento")
    hecho=models.BooleanField(default=False,null=False,verbose_name="Hecho")

    def __str__(self):
        return self.nombre
    
    def get_image(self):
        if self.imagen:
            return self.imagen.url
        return self.imagen.url