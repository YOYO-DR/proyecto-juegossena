from django.views.generic import ListView
from apps.info.models import PreguntaAyuda

class PreguntasAyudaView(ListView):
  model=PreguntaAyuda
  template_name="ayuda.html"