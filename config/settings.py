"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path

from config.db import MYSQL, SQLITE
from config.dictChannels import CHANNELS_AZURE, CHANNELS_LOCAL

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-07@aoydkpwh*_oq)ir#wzs^6r3ut)djnp0zp-^a$6o_54c-05o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# el segundo es la ip local del pc
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #libs
    'widget_tweaks',
    "channels",
    #Mis apps
    'apps.blogs',
    'apps.dispositivos',
    'apps.juegos',
    'apps.usuarios',
    'apps.chat',
    'apps.info'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': { 
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
# configuracion channels
ASGI_APPLICATION = 'config.asgi.application'
CHANNEL_LAYERS = CHANNELS_AZURE
#chat cantidad de mensajes (int)
CHAT_CANT_MSJ=20
# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = MYSQL


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'es-419'

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# configurando carpeta de mis archivos estaticos
STATICFILES_DIRS = [
  os.path.join(BASE_DIR,"static")
  ]

STATIC_URL = '/static/'

# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

#media
#carpeta donde se van a guardar los archivos subidos
if not 'WEBSITE_HOSTNAME' in os.environ:
  MEDIA_ROOT = os.path.join(BASE_DIR,'media')

#link de como se accede a ellos de forma publica
MEDIA_URL = 'media/'
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# clase usuario modificada
AUTH_USER_MODEL = 'usuarios.Usuario'

# despues de que cierre sesión
LOGOUT_REDIRECT_URL = 'usuarios:iniciarsesion'

# despues de iniciar sesion con el LoginView
LOGIN_REDIRECT_URL = 'inicio'

# por si dentra a una vista que requiera que el usuario inicie sesión
LOGIN_URL = 'usuarios:iniciarsesion'


# confirgurar servidor para enviar correos
# host del envio de correos
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
if 'WEBSITE_HOSTNAME' in os.environ: 
    config_email_tienda=os.environ['EMAIL_SEND']
    config_email_tienda_valores={i.split('=')[0]:i.split('=')[1] for i in config_email_tienda.split(' ')}
else:
    config_email_tienda_valores={
        'email':os.environ.get('CORREO'),
        'password':os.environ.get('PASS_CORREO')
    }
# correo de gmail que va a enviar correos
EMAIL_HOST_USER = config_email_tienda_valores['email']
# la contraseña
EMAIL_HOST_PASSWORD = config_email_tienda_valores['password']
EMAIL_USE_TLS = True

# url local
URL_LOCAL="http://192.168.110.39:8000"

# blob azure
STATIC_URL_AZURE="https://djangoyoiner.blob.core.windows.net/juegossena/static/"