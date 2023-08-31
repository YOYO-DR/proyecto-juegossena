from django.urls import path
from .views import BuscarJuegosView, InicioView
from django.contrib.auth.views import LogoutView

app_name='juegos'

urlpatterns = [
    path("buscar/",BuscarJuegosView.as_view(),name="buscar")
]
