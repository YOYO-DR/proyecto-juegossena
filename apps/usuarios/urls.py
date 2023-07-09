from django.urls import path
from .views import RegitroView,IniciarSesionView,OlvidoContraEmailView,CambioContraView
from django.contrib.auth.views import LogoutView

app_name='usuarios'

urlpatterns = [
    path('registro/',RegitroView.as_view(),name='registro'),
    path('iniciarsesion/',IniciarSesionView.as_view(),name='iniciarsesion'),
    path('cerrar/',LogoutView.as_view(),name='cerrar'),
    path('olvidoContra/',OlvidoContraEmailView.as_view(),name='olvidoContra'),
    path('cambioContra/<uidb64>/<token>/',CambioContraView.as_view(),name='cambioContra'),
]
