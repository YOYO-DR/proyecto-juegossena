from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import View,ListView

from apps.dispositivos.funciones import guardarCara, obtenerCara
from apps.dispositivos.models import Dispositivos
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import json

class ProcesarDatos(View):
    def dispatch(self, request, *args, **kwargs):
        if request.method=='GET':
           inicio = reverse_lazy('usuarios:iniciarsesion')
           return HttpResponseRedirect(inicio)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data={}
        archivo=request.FILES.get('archivo',"")
        if archivo=="":
            return JsonResponse({"error": "No se envio un archivo"})
        nombreArchivo=archivo.name.rstrip(".txt")
        # pregunto si viene el valor "reemplazar"
        if "reemplazar" not in request.POST:
          nombreDispo=nombreArchivo+"_"+str(request.user.id)
          dispositivosUsuario=Dispositivos.objects.filter(nombre=nombreDispo,usuario=request.user)
          if dispositivosUsuario.exists():
              return JsonResponse({"error": f"dipositivo ya existe {archivo.name}"})
        try:
          # cuando le aplico el readlines(), python automaticamente cierra el archivo
          lineas=archivo.readlines()
        except Exception as e:
            return JsonResponse({'error':str(e)})
        dataArchivo = []
        es_cpuz=False
        for linea in lineas:
           linea_decodificada=linea.decode('utf-8',errors='ignore')
           if "CPU-Z TXT Report" in linea_decodificada.strip():
             es_cpuz=True
           dataArchivo.append(linea_decodificada)
        if not es_cpuz:
          return JsonResponse({"error": "No es un archivo de CPU-Z"})
        cara=obtenerCara(dataArchivo)
        dispositivo=guardarCara(cara,request.user.id,nombreArchivo)
        data['nombre']=dispositivo.nombre
        data['id']=dispositivo.id
        return JsonResponse(data)

class DispositivosView(ListView):
    model = Dispositivos
    template_name = "adminDispo.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data={}
        dataValores=json.loads(request.body)
        try:
          action=dataValores.get("action")
          if action=="datosDispo":
              d=Dispositivos.objects.get(id=dataValores.get("id"),usuario=request.user)
              # le envio el json con los datos del dispositivo
              data['dispositivo']=d.json
              data['nombre']=d.nombre
          elif action=="eliminar":
              d=Dispositivos.objects.get(id=dataValores.get("id"))
              d.delete()
              data['eliminacion']=True
          else:
              data['error']="No se envio una acción"
        except Dispositivos.DoesNotExist as e:
            data={}
            data['error']="El dispositivo no existe"
        except Exception as e:
            data={}
            data["error"]=str(e)
        return JsonResponse(data)

    def get_queryset(self):
        query=Dispositivos.objects.filter(usuario_id=self.request.user.id)
        return query
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Dispositivos"
        return context
