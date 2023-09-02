from django.urls import path
from .views import BuscarJuegosView, DetalleJuegoView

app_name='juegos'

urlpatterns = [
    path("buscar/",BuscarJuegosView.as_view(),name="buscar"),
    path("detalle/<slug>",DetalleJuegoView.as_view(),name="detalle_juego"),
]
