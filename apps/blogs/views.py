from time import sleep
from typing import Any, Dict
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from apps.usuarios.models import Usuario
from apps.blogs.models import Requerimientos

class BlogsInicioView(TemplateView):
  template_name="blogs/inicio.html"

class RequerimientosView(TemplateView):
  template_name="blogs/requerimientos.html"

  def post(self, request, *args, **kwargs):
    datos={}
    try:
      requi=[]
      for value in request.POST.values():
        requi.append(int(value))
      for requisito in Requerimientos.objects.all():
        requisito.hecho = True if int(requisito.id) in requi else False
        requisito.save()
    except Exception as e:
      datos['error'] = str(e)

    return JsonResponse(datos)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    try:
      usuario = Usuario.objects.get(id=self.request.user.id)
    except:
      usuario=None
    admins=["duranyoiner86@gmail.com","breynnerper18@gmail.com","danielalexanderrojasquisacue2@gmail.com"]
    if usuario:
      if usuario.is_authenticated:
        if usuario.email in admins:
          context['es_admin']=True
    context['requi']=Requerimientos.objects.all()
    return context