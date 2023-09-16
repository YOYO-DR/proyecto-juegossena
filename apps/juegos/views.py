import json
from django.http import JsonResponse
from django.views.generic import TemplateView,View,DetailView
from apps.dispositivos.funciones import potenciaDispoJuego
from apps.dispositivos.models import Dispositivos, Favoritos, Juegos
from apps.juegos.funciones import filtroJuegos

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

class InicioView(TemplateView):
  template_name = 'index.html'

  def post(self, request, *args, **kwargs):
    data={}
    try:
      datos=json.loads(request.body)
    except Exception as e:
      print(str(e))
      return JsonResponse(data)
    try:
      juego=Juegos.objects.get(slug=datos['juego'])
      juego.cantidadVisitas+=1
      juego.save()
    except Exception as e:
      print(str(e))
    return JsonResponse(data)

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context["titulo"] = 'Inicio'
      context['juegos']=Juegos.objects.all()
      context['juegos_mas']=Juegos.objects.all().order_by("-cantidadVisitas")[0:10]
      return context

class DetalleJuegoView(DetailView):
  template_name="detalle_juego.html"
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
      if not request.user.is_authenticated:
        data['error']="no-auth"
      else:
        # no utilizo el favoritos_set porque eso es para el ForeignKeyField, en este caso utilizo el OneToOneField entonces en el usuario puedo acceder a el con "favoritos" y directo a su atributo juegos porque es el unico que tiene el usuario
        if request.user.favoritos.juegos.filter(nombre=self.get_object().nombre).exists():
          request.user.favoritos.juegos.remove(self.get_object())
          data['fav']="quitado"
        else:
          request.user.favoritos.juegos.add(self.get_object())
          data['fav']="agregado"
    else:
       data['error']="No se envio una acción (action)"
    
    return JsonResponse(data)

  
  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context["titulo"] = self.get_object().nombre
      context["img_juego"] = [i.get_imagen() for i in self.get_object().imagenesjuego_set.all()]
      # accedo a los favoritos del usuario, selecciono el primero y unico '[0]', y accedo a los juegos y aplico un filter buscando el juego y pregunto si existe el juego en esa lista (o bueno, queryset)
      if self.request.user.is_authenticated:
        context['en_fav']=self.request.user.favoritos.juegos.filter(nombre=self.get_object().nombre).exists()
      return context

class JuegosFavoritosView(TemplateView):
  template_name="favoritos.html"

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context["titulo"] = "Favoritos"
      context['juegos']=Favoritos.objects.get(usuario_id=self.request.user.id).juegos.all()
      return context

class BuscarJuegosDispoView(TemplateView):
  template_name="buscar_juegos.html"

  def dispatch(self, request, *args, **kwargs):
      return super().dispatch(request, *args, **kwargs)
  
  def post(self, request, *args, **kwargs):
    data={}
    try:
      datos=json.loads(request.body)
    except Exception as e:
      print(e)
      data["error"]=str(e)
      return JsonResponse(data)
    try:
      checkbox=datos["checkbox"]
      dispo_id=datos["dispo"]['id']
      busqueda=datos['busqueda']
    except Exception as e:
      print(str(e))
      data["error"]="No se enviaron todos los datos, error: " + str(e)
      return JsonResponse(data)
    # obtener dispositivo del usuario
    try:
      dispositivo=Dispositivos.objects.get(id=dispo_id,usuario_id=request.user.id)
    except Exception as e:
       print(e)
       data["error"]=str(e)
       return JsonResponse(data)
    # traer los juegos segun la busqueda y compararlo con el dispositivo y retornar el juego segun las opciones de los checkbox y el retorno de la funcion
    # potenciaDispoJuego
    # data['juegos']=[juego.toJSON() for juego in Juegos.objects.filter(nombre__icontains=busqueda)]
    data['juegos']=filtroJuegos(dispositivo,busqueda,checkbox)

    return JsonResponse(data)

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['dispositivos']=Dispositivos.objects.filter(usuario_id=self.request.user.id)
      return context
