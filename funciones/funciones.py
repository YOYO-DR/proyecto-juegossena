import ast
from django.contrib.sessions.models import Session

import os
# patron correo
from django.core.validators import validate_email

#validar contra
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

# correo
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from config.settings import EMAIL_HOST_USER

#verificar la sesion del usuario con su sesion id
def verificar_sesion(session_id):
    try:
        session = Session.objects.get(session_key=session_id)
        data = session.get_decoded()
        user_id = data.get('_auth_user_id', None)
        return user_id
    except Session.DoesNotExist:
        return None

def validar_patron_correo(email):
    try:
        validate_email(email)
        return True
    except:
        return False

def validar_contra(contra, usuario=None):
    try:
        validate_password(contra, usuario)
        return [True]
    except ValidationError as e:
        errors = e.error_list
        errores = []
        for error in errors:
            # como retorna algo como "['error']", con ast analizo el string, y lo convierto a lista y luego accedo a su valor 0
            error=ast.literal_eval(str(error))[0]
            errores.append(error)
        return [False, errores]

def enviarEmailActivacion(dominio,usuario):
  email=usuario.email
  if 'WEBSITE_HOSTNAME' in os.environ:
      dominio = 'https://'+str(dominio)
  else:
      dominio = 'http://'+str(dominio)
  asunto = 'Activar cuenta'
  cuerpoMensaje = render_to_string('emails/email_activarCuenta.html',{
      'usuario':usuario,
      'dominio':dominio,
      'uid':urlsafe_base64_encode(force_bytes(usuario.pk)),
      'token':default_token_generator.make_token(usuario)
  })
  toEmail = email
  envioEmail = EmailMultiAlternatives(asunto, '', to=[toEmail],from_email=f"Juegos Sena <{EMAIL_HOST_USER}>")
  #luego con esa funcion le paso el html y le digo que va a ser un html
  envioEmail.attach_alternative(cuerpoMensaje, "text/html")
  envioEmail.send()