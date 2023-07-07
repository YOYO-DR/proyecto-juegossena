from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views import View

from apps.dispositivos.functions import guardarCara, obtenerCara


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
        guardarCara(cara)
        return JsonResponse(cara)