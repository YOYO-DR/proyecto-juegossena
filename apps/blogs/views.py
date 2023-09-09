from django.http import JsonResponse
from django.views.generic import TemplateView,DetailView
from apps.usuarios.models import Usuario
from apps.blogs.models import Blogs, Requerimientos

class BlogsInicioView(TemplateView):
  template_name="inicio.html"

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context["blogs"] = Blogs.objects.all()
      return context

class BlogDetailView(DetailView):
  template_name="blog_detail.html"

  def get_queryset(self):
      return Blogs.objects.filter(slug=self.kwargs.get("slug"))

class RequerimientosView(TemplateView):
  template_name="requerimientos.html"

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