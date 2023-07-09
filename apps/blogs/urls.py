from django.urls import path
from apps.blogs.views import BlogsInicioView, RequerimientosView

app_name='blogs'

urlpatterns = [
    path('',BlogsInicioView.as_view(),name="inicio"),
    path('requerimientos/',RequerimientosView.as_view(),name="requerimientos"),
]