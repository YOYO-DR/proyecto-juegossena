import json
from django.http import JsonResponse
from django.views.generic import TemplateView,View
from apps.dispositivos.models import Juegos

#vista peticiones de busqueda

class BuscarJuegosView(View):
   def post(self, request, *args, **kwargs):
      data={}
      try:
        # llega por json la busqueda
        busqueda=json.loads(request.body)
        busqueda=busqueda.get('busqueda',"")
      except Exception as e:
         data['error']=str(e)
      data['juegos']=[i.toJSON() for i in Juegos.objects.filter(nombre__icontains=busqueda)]
      return JsonResponse(data)

# inicio
class InicioView(TemplateView):
  template_name = 'index.html'

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context["titulo"] = 'Inicio'
      context['juegos']=Juegos.objects.all()
      context['juegos_mas']=Juegos.objects.all().order_by("-cantidadVisitas")[0:10]
      return context
