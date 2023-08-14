from django.shortcuts import render
from django.views.generic import TemplateView
from apps.dispositivos.models import Juegos

class InicioView(TemplateView): 
  template_name = 'index.html'

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context["titulo"] = 'Inicio'
      return context


def prueba(request):
   return render(request,'plantillas/prueba.html')