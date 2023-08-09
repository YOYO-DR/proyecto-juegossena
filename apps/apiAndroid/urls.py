from django.urls import path

from apps.apiAndroid.views import CerrarSesionView, DatosDispositivosApi, DatosUsuarioApi, InicioSesionApi, RegistrarUsuarioApi

app_name="apiAndroid"

urlpatterns = [
    path('iniciosesionapi/',InicioSesionApi.as_view(),name='iniciosesionapi'),
    path('cerrarsesionapi/',CerrarSesionView.as_view(),name='cerrarsesionapi'),
    path('registrarusuarionapi/',RegistrarUsuarioApi.as_view(),name='registrarusuarionapi'),
    path('datosusuarioapi/',DatosUsuarioApi.as_view(),name='datosusuarioapi'),
    path('datosdispositivosapi/',DatosDispositivosApi.as_view(),name='datosdispositivosapi'),
]
