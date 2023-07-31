from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import authenticate, login,logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from apps.apiAndroid.funciones import verificar_sesion
from apps.usuarios.models import Usuario
from django.contrib.sessions.models import Session

class InicioSesionApi(View):
    #quitar seguridad del token
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request,*args, **kwargs):
        data={}
        action = request.POST.get('action')
        if action=="iniciarsesion":
          try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            if username and password:
              if Usuario.objects.filter(username=username).exists():
                user=authenticate(request, username=username, password=password)
                if user is not None:
                  login(request, user)
                  data['sessionid']=request.session.session_key
                else:
                  data['error']=["Contraseña incorrecta"]
              else:
                data['error']=["El usuario no existe"]
            else:
              data['error']=[]
              if not username:
                data['error'].append("No se envio un nombre de usuario")
              if not password:
                 data['error'].append("No se envio la contraseña")
          except Exception as e:
             data['error']=["Hubo un error: "+str(e)]
        elif action=="verificariniciarsesion":
          id_usuario=verificar_sesion(request.POST.get("session_id"))
          if id_usuario is not None:
             data['validacion']="true"
          else:
             data['validacion']="false"
        return JsonResponse(data)

class CerrarSesionView(View):
   #quitar seguridad del token
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
      data={}
      action=request.POST.get('action')
      if action=="cerrarsesion":
        id_usuario=verificar_sesion(request.POST.get('session_id'))
        if id_usuario is not None:
          # Borra e inhavilito el session_id
          Session.objects.get(session_key=request.POST.get('session_id')).delete()
          data['respuesta']=["true"]
        else:
          data['respuesta']=["sesion invalida"]
      return JsonResponse(data)