from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import HistorialChat

class ChatView(TemplateView):
    template_name="chat/chat.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["room_name"] = "social"
        historial=[]
        historialDiasFechas=HistorialChat.diasRegistros()
        for i in historialDiasFechas[0]:
          # en la funcion diasRegistros, obtengo los registros, les modifico su datetime al que quiero, y retorno los dias sin repetirce y los registros modificados
          #aqui en el for recorro los registros y luego pregunto si la fecha (yyyy-mm-dd) se encuenta en la fecha del objeto en cuestion y si lo esta, lo guarda, de lo contrario, no
          registros=[j.toJSON() for j in historialDiasFechas[1] if str(i) in str(j.datetime.date())]
          historial.append({"dia":i,"registros":registros})
        context['historial']=historial
        return context