from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView,View
from apps.dispositivos.models import Juegos

#vista peticiones de busqueda

class BuscarJuegosView(View):
   def post(self, request, *args, **kwargs):
      data={}
      busqueda=request.POST.get("busqueda","")
      data['juegos']=[i.toJSON() for i in Juegos.objects.filter(nombre__icontains=busqueda)[0:10]]
      return JsonResponse(data)


# inicio
class InicioView(TemplateView): 
  template_name = 'index.html'

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context["titulo"] = 'Inicio'
      return context
