from collections.abc import Iterable
import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from config.settings import MEDIA_URL,STATIC_URL, STATIC_URL_AZURE


class Usuario(AbstractUser):
    email = models.EmailField(null=False, blank=False,unique=True,verbose_name='Correo electrónico')
    imagen=models.ImageField(upload_to=f'{MEDIA_URL}users/%Y/%m/' if 'WEBSITE_HOSTNAME' in os.environ else 'users/%Y/%m/',null=True,blank=True, verbose_name='Foto de perfil')
    is_active = models.BooleanField(default=False)

    def get_imagen(self):
        if self.imagen:
            return self.imagen.url
        return f'{STATIC_URL_AZURE}media/img/empty.png' if 'WEBSITE_HOSTNAME' in os.environ else f'{STATIC_URL}media/img/empty.png'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.is_superuser and not self.pk:
            self.is_active=True
        return super(Usuario, self).save()

