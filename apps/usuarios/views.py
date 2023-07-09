import json
import os
from django.contrib.auth import authenticate, login
# from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from django.core.mail import EmailMultiAlternatives

from apps.usuarios.models import Usuario
from .forms import crearUsuarioForm

from .forms import IniciarSesionForm, crearUsuarioForm

#correo
from .funciones import validar_patron_correo,validar_contra
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage

class RegitroView(FormView):
  form_class = crearUsuarioForm
  template_name = 'usuarios/registro.html'
  success_url = reverse_lazy('inicio')

  def dispatch(self, request, *args, **kwargs):
    #antes de entrar a la pagina reviso que no este autenticado, si lo esta, lo mando al inicio
    if request.user.is_authenticated:
      return redirect('inicio')
    return super().dispatch(request, *args, **kwargs)

  def form_valid(self, form):
    form.save()
    user = form.cleaned_data['username']
    passw = form.cleaned_data['password1']
    user=authenticate(username=user, password=passw)
    #si es correcto el formulario, inicio sesión
    login(self.request, user)
    return HttpResponseRedirect(self.success_url)
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['title'] = 'Iniciar sesión'
    return context

class IniciarSesionView(FormView):
  form_class = IniciarSesionForm
  template_name = 'usuarios/iniciarSesion.html'
  success_url = reverse_lazy('inicio')

  def form_valid(self, form):
    login(self.request, form.get_user())

    #enviar correo
    usuario=self.request.user
    email=usuario.email
    dominio = get_current_site(self.request)
    if 'WEBSITE_HOSTNAME' in os.environ:
        dominio = 'https://'+str(dominio)
    else:
        dominio = 'http://'+str(dominio)
    mail_subject = 'Inicio de sesión correcto'
    body = render_to_string('usuarios/emails/email_iniciosesion.html',{
       # data para manipular en el html
        'usuario':usuario,
        'dominio':dominio
    })
    to_email = email
    #este envia un mensaje normal
    # send_email=EmailMessage(mail_subject, body,to=[to_email])
    #pero para html, lo hago de la siguiente forma
    #le paso el asunto, las comillas vacias son para enviar texto plano, por si depronto el mail no puede renderizar el html, y si no se quiere pasar, solo se dejan vacias, y luego a donde se va a enviar en un arreglo
    send_email = EmailMultiAlternatives(mail_subject, '', to=[to_email])
    #luego con esa funcion le paso el html y le digo que va a ser un html
    send_email.attach_alternative(body, "text/html")
    send_email.send()

    return HttpResponseRedirect(self.success_url)
  
  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context["titulo"] = 'Iniciar sesión'
      return context

class OlvidoContraEmailView(TemplateView):
  template_name="usuarios/olvidoContra.html"

  def post(self, request, *args, **kwargs):
    datos={}
    #pregunto si se esta enviando el correo
    if request.POST.get('email'):
      #si existe, lo almaceno
      email = request.POST.get('email')
      print(f'"{email}"')
      #valido si es correcto
      if not validar_patron_correo(email):
        datos['error'] = "Debe ingresar un correo valido"
      else:
        # pregunto si existe un usuario con ese correo
        if not Usuario.objects.filter(email=email).exists():
          datos['error'] = "No existe un usuario con ese correo"
        else:
          #obtengo el usuario con ese correo
          usuario=Usuario.objects.get(email=email)
          #enviar correo
          dominio = get_current_site(request)
          if 'WEBSITE_HOSTNAME' in os.environ:
              dominio = 'https://'+str(dominio)
          else:
              dominio = 'http://'+str(dominio)
          asunto = 'Cambiar contraseña'
          cuerpoMensaje = render_to_string('usuarios/emails/email_olvidoContra.html',{
              'usuario':usuario,
              'dominio':dominio,
              'uid':urlsafe_base64_encode(force_bytes(usuario.pk)),
              'token':default_token_generator.make_token(usuario)
          })
          toEmail = email
          envioEmail = EmailMultiAlternatives(asunto, '', to=[toEmail])
          #luego con esa funcion le paso el html y le digo que va a ser un html
          envioEmail.attach_alternative(cuerpoMensaje, "text/html")
          envioEmail.send()
    else:
      datos['error']="Debe ingresar un correo"

    return JsonResponse(datos)

class CambioContraView(TemplateView):
  template_name = "usuarios/cambiarContra.html"

  def dispatch(self, request, *args, **kwargs):
      if request.method == 'GET':
        uidb64=kwargs.get('uidb64')
        token=kwargs.get('token')
        try:
          #decodifico el uidb64 y obtengo el usuario segun el uid
          uid = urlsafe_base64_decode(uidb64).decode()
          usuario = Usuario.objects.get(pk=uid)
        except (TypeError, ValueError,OverflowError, Usuario.DoesNotExist):
          # si sale algun error, dejo el usuario como None
          usuario = None
        #si existe un usuario y el token es correcto, lo dejo entrar a la pagina
        #el token se va a invalidar cuando se le cambie la contraseña al usuario relacionado
        if usuario is not None and default_token_generator.check_token(usuario,token):
          pass
        # si ya expiro el token
        else:
          return redirect('inicio')
      return super().dispatch(request, *args, **kwargs)
  
  def post(self, request, *args, **kwargs):
    uid = urlsafe_base64_decode(kwargs.get('uidb64')).decode()
    usuario=Usuario.objects.get(pk=uid)
    datos={}

    if not (request.POST.get('contra') and request.POST.get('contra_confirm')):
      #si estan vacias las contraseñas
      datos['error']="Las contraseñas no pueden estar vacias"
    else:
      #obtengo las contraseña ingresadas
      contra=request.POST.get('contra')
      contraConfirm=request.POST.get('contra_confirm')
      #verifico que sean iguales
      if contra != contraConfirm:
        datos['error']="Las contraseñas no coinciden"
      else:
        #valido la contraseña con el usuario para que no tenga cosas parecidas a sus datos
        validacionContra=validar_contra(contra,usuario)
        if not validacionContra[0]:
          #si hay errores en la verificacion
          if len(validacionContra[1])>1:
            mensaje=', '.join(validacionContra[1])
          else:
            mensaje=validacionContra[1][0]
          datos['error']=mensaje
        else:
          #cambio la contraseña
          usuario.set_password(contra)
          usuario.save()
    return JsonResponse(datos)

