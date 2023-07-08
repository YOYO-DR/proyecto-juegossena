from django.contrib.auth import authenticate, login
# from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import crearUsuarioForm

from .forms import IniciarSesionForm, crearUsuarioForm


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
    return HttpResponseRedirect(self.success_url)
  
  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context["titulo"] = 'Iniciar sesión'
      return context
