from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import View,ListView

from apps.dispositivos.functions import guardarCara, obtenerCara
from apps.dispositivos.models import Dispositivos
from apps.usuarios.models import Usuario
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

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

    def get_queryset(self):
        query=Dispositivos.objects.filter(usuario_id=self.request.user.id)
        return query