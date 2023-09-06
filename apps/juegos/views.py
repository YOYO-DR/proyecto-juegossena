import json
from django.http import JsonResponse
from django.views.generic import TemplateView,View,DetailView
from apps.dispositivos.models import Favoritos, Juegos

#vista peticiones de busqueda

class BuscarJuegosView(View):
   def post(self, request, *args, **kwargs):
      data={}
      try:
        # llega por json la busqueda
        datos=json.loads(request.body)
      except Exception as e:
         data['error']=str(e)
      action=datos.get("action","")
      # si se va a realizar la busqueda
      if action=="busqueda":
        busqueda=datos.get('busqueda',"")
        data['juegos']=[i.toJSON() for i in Juegos.objects.filter(nombre__icontains=busqueda)]
      # buscar juego en expecifico por su slug
      elif action=="buscar_juego":
        try:
          data['juego']=Juegos.objects.get(slug=datos['slug']).toJSON()
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

  def post(self, request, *args, **kwargs):
    data={}
    try:
      # llega por json la busqueda
      datos=json.loads(request.body)
    except Exception as e:
      data['error']=str(e)
    action=datos.get("action","")

    if action=="requisitos":
      data['juego']=self.get_object().requisitos()
    elif action=="agrefav":
      favoritos,creado=Favoritos.objects.get_or_create(usuario_id=request.user.id)
      if favoritos.juegos.filter(nombre=self.get_object().nombre).exists():
        favoritos.juegos.remove(self.get_object())
        data['fav']="quitado"
      else:
        favoritos.juegos.add(self.get_object())
        data['fav']="agregado"
    else:
       data['error']="No se envio una acción (action)"
    
    return JsonResponse(data)

  
  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context["titulo"] = self.get_object().nombre
      context["img_juego"] = [i.get_imagen() for i in self.get_object().imagenesjuego_set.all()]
      # accedo a los favoritos del usuario, selecciono el primero y unico '[0]', y accedo a los juegos y aplico un filter buscando el juego y pregunto si existe el juego en esa lista (o bueno, queryset) 
      context['en_fav']=self.request.user.favoritos_set.all()[0].juegos.filter(nombre=self.get_object().nombre).exists()
      return context