from django.urls import path

from apps.info.views import PreguntasAyudaView

app_name='info'

urlpatterns = [
    path("ayuda/",PreguntasAyudaView.as_view(),name="preguntas_ayuda")
]
