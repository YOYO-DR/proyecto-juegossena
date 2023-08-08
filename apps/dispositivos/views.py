from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import View,ListView

from apps.dispositivos.functions import guardarCara, obtenerCara
from apps.dispositivos.models import Dispositivos
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json

class ProcesarDatos(View):
    def dispatch(self, request, *args, **kwargs):
        if request.method=='GET':
           inicio = reverse_lazy('usuarios:iniciarsesion')
           return HttpResponseRedirect(inicio)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        archivo=request.FILES['archivo']
        lineas=archivo.readlines()
        data = []
        for linea in lineas:
           linea_decodificada=linea.decode('utf-8',errors='ignore')
           data.append(linea_decodificada)
        cara=obtenerCara(data)
        nombreArchivo=archivo.name.rstrip(".txt")
        guardarCara(cara,request.user.id,nombreArchivo)
        return JsonResponse(cara)


class DispositivosView(ListView):
    model = Dispositivos
    template_name = "dispositivos/adminDispo.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data={}
        dataValores=json.loads(request.body)
        try:
          action=dataValores.get("action")
          if action=="datosDispo":
              d=Dispositivos.objects.get(id=dataValores.get("id"))
              data['dispositivo']=d.toJSON()
          elif action=="eliminar":
              d=Dispositivos.objects.get(id=dataValores.get("id"))
              d.delete()
              data['eliminacion']=True
          else:
              data['error']="No se envio una acción"
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
    