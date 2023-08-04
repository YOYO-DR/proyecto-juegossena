import os
from django.http import JsonResponse
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from funciones.funciones import enviarEmailActivacion, validar_contra, validar_patron_correo, verificar_sesion
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
      id_usuario=verificar_sesion(request.POST.get('session_id'))
      if id_usuario is not None:
        # Borra e inhavilito el session_id
        Session.objects.get(session_key=request.POST.get('session_id')).delete()
        data['respuesta']=["true"]
      else:
        data['respuesta']=["sesion invalida"]
      return JsonResponse(data)

class RegistrarUsuarioApi(View):
  #quitar seguridad del token
  @method_decorator(csrf_exempt)
  def dispatch(self, request, *args, **kwargs):
      return super().dispatch(request, *args, **kwargs)
  
  def post(self, request, *args, **kwargs):
    data={}
    valoresUsuario={}
    valoresUsuario["nombre"]=request.POST.get('nombre',"")
    valoresUsuario["email"]=request.POST.get('email',"")
    valoresUsuario['contra']=request.POST.get('contra',"")
    valoresUsuario['contraConfirm']=request.POST.get('contraConfirm',"")
    # verifico si existe algun valor vacion, si existe, creo la clave error como arreglo
    for valor in valoresUsuario.values():
       if valor=="":
          data['error']=[]
          break
    # pregunto si se creo la clave error
    if 'error' in data:
      # si existe la clave error, recorro los valores obtenidos y pregunto cual tiene valores vacios y agrego el error
      for clave,valor in valoresUsuario.items():
        print(f'clave: {clave} - valor: {valor}')
        if valor=="":
          data['error'].append(f'{clave} vacia')
    if "error" not in data:
      #verifico que no exista el usuario
      if Usuario.objects.filter(username=valoresUsuario['nombre']).exists():
         data['error']=['El usuario ya existe']
      #verifico el patron del email
      elif not validar_patron_correo(valoresUsuario['email']):
        data['error']=['Email invalido']
      # verifico si el email existe
      elif Usuario.objects.filter(email=valoresUsuario['email']).exists():
         data['error']=['Ya existe un usuario con ese email']
      # verifico que las contraseñan coinciden
      elif valoresUsuario['contra'] != valoresUsuario['contraConfirm']:
        data['error'] = ['Las contraseñas no coinciden']
      #verificar el patron de la contraseña
      elif not validar_contra(valoresUsuario['contra'])[0]:
        data['error']=validar_contra(valoresUsuario['contra'])[1]
      else:
        # si no hay errores creo el usuario
        data["respuesta"]=''
        try:
          usuario=Usuario()
          usuario.username=valoresUsuario['nombre']
          usuario.email=valoresUsuario['email']
          usuario.set_password(valoresUsuario['contra'])
          usuario.save()
          if 'WEBSITE_HOSTNAME' in os.environ:
            dominio = "juegossena.azurewebsites.net"
          else:
            dominio = '192.168.110.39:8000'
          enviarEmailActivacion(dominio,usuario=usuario)
          data['respuesta']=["usuario creado",usuario.email]
        except Exception as e:
           data['error']=[str(e)]

    return JsonResponse(data)