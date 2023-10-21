import json
from django.http import JsonResponse
from django.views.generic import ListView
from apps.info.models import PreguntaAyuda

class PreguntasAyudaView(ListView):
  model=PreguntaAyuda
  template_name="ayuda.html"

  def post(self, request, *args, **kwargs):
    data={}
    datos=json.loads(request.body)
    try:
      data=PreguntaAyuda.objects.get(id=datos.get('id')).toJSON()
    except Exception as e:
      print(str(e))
      data['error']=str(e)
    return JsonResponse(data)