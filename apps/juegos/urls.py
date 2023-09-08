from django.urls import path
from .views import BuscarJuegosDispoView, BuscarJuegosView, DetalleJuegoView,JuegosFavoritosView

app_name='juegos'

urlpatterns = [
    path("buscar/",BuscarJuegosView.as_view(),name="buscar"),
    path("detalle/<slug>/",DetalleJuegoView.as_view(),name="detalle_juego"),
    path("favoritos/",JuegosFavoritosView.as_view(),name="juegos_favoritos"),
    path("buscar-juegos/",BuscarJuegosDispoView.as_view(),name="buscar_juegos"),
]
