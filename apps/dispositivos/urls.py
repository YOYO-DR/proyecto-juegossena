from django.urls import path

from apps.dispositivos.views import ProcesarDatos

app_name='dispositivos'

urlpatterns = [
    path('',ProcesarDatos.as_view(), name='procesar'),
]
