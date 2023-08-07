from django.urls import path

from apps.dispositivos.views import DispositivosView, ProcesarDatos

app_name='dispositivos'

urlpatterns = [
    path('inicio/',DispositivosView.as_view(), name='inicio'),
    path('procesar/',ProcesarDatos.as_view(), name='procesar'),
]
