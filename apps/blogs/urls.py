from django.urls import path
from apps.blogs.views import BlogDetailView, BlogsInicioView, RequerimientosView

app_name='blogs'

urlpatterns = [
  path('',BlogsInicioView.as_view(),name="inicio"),
  path('requerimientos/',RequerimientosView.as_view(),name="requerimientos"),
  path('<slug>/',BlogDetailView.as_view(),name="blog_detail"),
]