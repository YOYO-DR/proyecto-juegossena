from django.urls import path

from apps.apiAndroid.views import EmailUsuarioApi, InicioSesionApi

app_name="apiAndroid"

urlpatterns = [
    path('iniciosesionapi/',InicioSesionApi.as_view(),name='iniciosesionapi'),
    path('emailusuario/',EmailUsuarioApi.as_view(),name="emailusuario")
]
