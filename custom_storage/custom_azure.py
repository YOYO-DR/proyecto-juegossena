from storages.backends.azure_storage import AzureStorage
from config.production import azure_storage_blob_parametros
    
class PublicAzureStaticStorage(AzureStorage):
    account_name = azure_storage_blob_parametros['account_name']
    account_key = azure_storage_blob_parametros['account_key']
    azure_container = azure_storage_blob_parametros['container_name']
    location = 'static/'  # ubicación dentro del contenedor
    expiration_secs = None

# Configuración para los archivos de media
class PublicAzureMediaStorage(AzureStorage):
    account_name = azure_storage_blob_parametros['account_name']
    account_key = azure_storage_blob_parametros['account_key']
    azure_container = azure_storage_blob_parametros['container_name']
    location = 'media/'  # ubicación dentro del contenedor
    expiration_secs = None