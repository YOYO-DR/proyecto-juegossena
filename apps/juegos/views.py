import json
from django.http import JsonResponse
from django.views.generic import TemplateView,View,DetailView
from apps.dispositivos.models import Juegos

#vista peticiones de busqueda

class BuscarJuegosView(View):
   def post(self, request, *args, **kwargs):
      data={}
      try:
        # llega por json la busqueda
        datos=json.loads(request.body)
        busqueda=datos.get('busqueda',"")
      except Exception as e:
         data['error']=str(e)
      action=datos.get("action","")
      # si se va a realizar la busqueda
      if action=="busqueda":
        data['juegos']=[i.toJSON() for i in Juegos.objects.filter(nombre__icontains=busqueda)]
      # buscar juego en expecifico por su slug
      elif action=="buscar_juego" or action=="requisitos":
        try:
          juego=Juegos.objects.get(slug=datos['slug'])
          data['juego']=juego.toJSON() if action=="buscar_juego" else juego.requisitos()
        except Juegos.DoesNotExist as e:
           data['error']="El juego no existe."
        except Exception as e:
           data['error']=str(e)
      else:
         data['error']="No se envio una acción (action)"

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

class DetalleJuegoView(DetailView):
  template_name="juegos/detalle_juego.html"
  model=Juegos
  
  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context["titulo"] = self.get_object().nombre
      context["img_juego"] = [i.get_imagen() for i in self.get_object().imagenesjuego_set.all()]
      return context