from django.urls import path
from .views import InicioView,prueba
from django.contrib.auth.views import LogoutView

app_name='juegos'

urlpatterns = [
 path('prueba/',prueba)
]
