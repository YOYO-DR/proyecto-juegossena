from django.urls import path

from apps.apiAndroid.views import CerrarSesionView, InicioSesionApi

app_name="apiAndroid"

urlpatterns = [
    path('iniciosesionapi/',InicioSesionApi.as_view(),name='iniciosesionapi'),
    path('cerrarsesionapi/',CerrarSesionView.as_view(),name='cerrarsesionapi'),
]
