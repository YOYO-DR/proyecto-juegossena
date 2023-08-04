from django.shortcuts import render
from django.views.generic import TemplateView
from apps.dispositivos.models import Juegos

class InicioView(TemplateView): 
  template_name = 'juegos/inicio.html'

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context["titulo"] = 'Inicio'
      context["dato"] = 'Este va a ser la pagina inicial del proyecto'
      return context


def prueba(request):
   return render(request,'plantillas/prueba.html')