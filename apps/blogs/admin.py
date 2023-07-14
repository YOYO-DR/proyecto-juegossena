from django.contrib import admin
from apps.blogs.models import Blogs, Requerimientos

class BlogAdmin(admin.ModelAdmin):
  # para que autocomplete el slug con el titulo
  prepopulated_fields={'slug':("titulo",)}

admin.site.register(Requerimientos)
admin.site.register(Blogs,BlogAdmin)