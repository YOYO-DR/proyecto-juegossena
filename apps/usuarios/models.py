import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from config.settings import MEDIA_URL,STATIC_URL
STATIC_URL_AZURE="https://djangoyoiner.blob.core.windows.net/juegossena/static/"
STATIC_URL_LOCAL="http://192.168.110.39:8000/static/"
class Usuario(AbstractUser):
    email = models.EmailField(null=False, blank=False,unique=True,verbose_name='Correo electrónico')
    imagen=models.ImageField(upload_to=f'{MEDIA_URL}users/%Y/%m/' if 'WEBSITE_HOSTNAME' in os.environ else 'users/%Y/%m/',null=True,blank=True, verbose_name='Foto de perfil')
    is_active = models.BooleanField(default=False)

    def get_imagen(self):
        if self.imagen:
            return self.imagen.url
        return f'{STATIC_URL_AZURE}media/img/empty.png' if 'WEBSITE_HOSTNAME' in os.environ else f'{STATIC_URL_LOCAL}media/img/empty.png'