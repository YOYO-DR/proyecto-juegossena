from django.db import models
from django.contrib.auth.models import AbstractUser
from config.settings import MEDIA_URL,STATIC_URL
class Usuario(AbstractUser):
    email = models.EmailField(null=False, blank=False,unique=True,verbose_name='Correo electrónico')
    imagen=models.ImageField(upload_to=f'{MEDIA_URL}users/%Y/%m/',null=True,blank=True, verbose_name='Foto de perfil')
    is_active = models.BooleanField(default=False)

    def get_imagen(self):
        if self.imagen:
            return self.imagen.url
        return f'{STATIC_URL}media/img/empty.png'