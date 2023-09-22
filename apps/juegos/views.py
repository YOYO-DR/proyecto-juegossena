import json
from time import sleep
from django.http import JsonResponse
from django.views.generic import TemplateView,View,DetailView
from apps.dispositivos.models import Dispositivos, Favoritos, ImagenesJuego, Juegos
from apps.juegos.funciones import filtroJuegos
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

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

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
      return super().dispatch(request, *args, **kwargs)
  
  def post(self, request, *args, **kwargs):
    data={}
    try:
      datos=json.loads(request.body)
    except Exception as e:
      print(str(e))
      return JsonResponse({"error":str(e)})
    action=datos.get("action","")
    if action=="juegos":
      data["juegos"]=[juego.toJSON() for juego in Juegos.objects.filter(favoritos__usuario_id=request.user.id).order_by("nombre")]
    elif action=="imagenes":
      try:
        data['juego']=Juegos.objects.get(favoritos__usuario_id=request.user.id,slug=datos.get("slug")).toJSON()
      except Exception as e:
        print(str(e))
        return JsonResponse({"error":"Slug o usuario de juego invalido"})
        
      data['imagenes']=[img.get_imagen() for img in ImagenesJuego.objects.filter(juego_id=data['juego']["id"])]
    elif action=="eliminar":
      slug=datos.get("slug")
      # obtener juego
      try:
        juego=Juegos.objects.get(slug=slug)
        favorito=Favoritos.objects.get(usuario_id=request.user.id)

        # eliminar favorito del usuario
        favorito.juegos.remove(juego)
      except Juegos.DoesNotExist:
        return JsonResponse({"error":"Slug de juego invalido"})
      except Favoritos.DoesNotExist:
        return JsonResponse({"error":"Favorito de usuario invalido"})
      except Exception as e:
        print("error: "+str(e))
        return JsonResponse({"error":str(e)})
    else:
      return JsonResponse({"error":"No se envio una accion [action]"})
    return JsonResponse(data)

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
    data['dispo']=dispositivo.json
    data['juegos']=filtroJuegos(dispositivo,busqueda,checkbox)

    return JsonResponse(data)

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['dispositivos']=Dispositivos.objects.filter(usuario_id=self.request.user.id)
      return context
