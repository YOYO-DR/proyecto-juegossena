from django.contrib import admin
from .models import Telefonos,Favoritos,Historiales,RamsVelocidades,TipoRam,Rams,Procesadores,SistemasOperativos,GraficasGb,GraficasVelocidades,Graficas,Dispositivos,Juegos

admin.site.register(Juegos)
admin.site.register(Telefonos)
admin.site.register(Favoritos)
admin.site.register(Historiales)
admin.site.register(RamsVelocidades)
admin.site.register(Rams)
admin.site.register(Procesadores)
admin.site.register(SistemasOperativos)
admin.site.register(GraficasGb)
admin.site.register(GraficasVelocidades)
admin.site.register(Graficas)
admin.site.register(Dispositivos)
admin.site.register(TipoRam)