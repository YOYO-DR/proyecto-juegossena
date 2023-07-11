import os

from .settings import * #importamos todo
from .settings import BASE_DIR # importamos la ruta de inicio

# se agrega los host por medio de las variables de entono que me da Azure
ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []
#se pone las rutas de seguridad
CSRF_TRUSTED_ORIGINS = ['https://' + os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []

#ponemos el DEBUG en false porque se va a ejecutar en produccion
DEBUG = False

INSTALLED_APPS.append('storages')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Add whitenoise middleware after the security middleware
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
# agregamos el storage
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' 

#Pedimos la config de la base de datos 
conn_str = os.environ['AZURE_MYSQL_CONNECTIONSTRING']


#extraemos los valores, y los ponemos en un diccionario para llamarlos mejor
conn_str_params = {pair.split('=')[0]: pair.split('=')[1] for pair in conn_str.split(' ')}

#Este es el valor de la variable de entono que se utiliza en Azure, puede utilizarlas independientemente en azure si quiere, lo utilizao de esta forma para solo poner una sola variable de entorno

#AZURE_MYSQL_CONNECTIONSTRING = dbname=nombreBD host=elHost port=3306 sslmode=require user=usuario password=pass

#los ponemos en la config de la base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': conn_str_params['dbname'],
        'HOST': conn_str_params['host'],
        'USER': conn_str_params['user'],
        'PASSWORD': conn_str_params['password'],
    }
}

#AZURE_MYSQL_CONNECTIONSTRING = dbname=nombreBD host=elHost port=3306 sslmode=require user=usuario password=pass

#almacenmiento azure
# Configuración para el diccionario de storages
# si estamos en producción o desarrollo, y saber de donde traer la configuración

azure_storage_blob = os.environ['AZURE_STORAGE_BLOB']
azure_storage_blob_parametros = {parte.split(' = ')[0]:parte.split(' = ')[1] for parte in azure_storage_blob.split('  ')}

AZURE_CONTAINER = azure_storage_blob_parametros['container_name']
AZURE_ACCOUNT_NAME = azure_storage_blob_parametros['account_name']
AZURE_ACCOUNT_KEY = azure_storage_blob_parametros['account_key']
STORAGES = {
    "default": {"BACKEND": "storages.backends.azure_storage.AzureStorage"},
    "staticfiles": {"BACKEND": "custom_storage.custom_azure.PublicAzureStaticStorage"},
    "media": {"BACKEND": "custom_storage.custom_azure.PublicAzureMediaStorage"},
}
