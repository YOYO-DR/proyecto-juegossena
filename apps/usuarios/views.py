import os
from django.contrib.auth import authenticate, login
# from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView

from config.settings import EMAIL_HOST_USER
from django.core.mail import EmailMultiAlternatives
from .forms import crearUsuarioForm

from .forms import IniciarSesionForm, crearUsuarioForm

#correo
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
    current_site = get_current_site(self.request)
    if 'WEBSITE_HOSTNAME' in os.environ:
        current_site = 'https://'+str(current_site)
    else:
        current_site = 'http://'+str(current_site)
    mail_subject = 'Inicio de sesión correcto'
    body = render_to_string('usuarios/emails/email.html',{
       # data para manipular en el html
        'usuario':usuario,
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
