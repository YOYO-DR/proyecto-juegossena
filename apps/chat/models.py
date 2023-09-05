from django.db import models
from apps.funciones_gen import timezone_now_cre
from apps.usuarios.models import Usuario
from django.forms import model_to_dict

from config.settings import CHAT_CANT_MSJ, TIME_ZONE

class HistorialChat(models.Model):
  user=models.ForeignKey(Usuario,on_delete=models.CASCADE,verbose_name="Usuario")
  message=models.TextField(null=True, blank=True, verbose_name="Mensaje")
  # formato: 'YYYY-MM-DD HH:MM:SS'
  datetime=models.DateTimeField(auto_now_add=True,verbose_name="Fecha enviado")

  def __str__(self):
    return self.message

  def toJSON(self):
    item=model_to_dict(self)
    item['user'] = {"id":self.user.id, "username":self.user.username}
    # agrego una key para no modificar el original, y le aplico un formato para que aparezca de 0 a 12 y con su pm y am
    item['datetime']=timezone_now_cre(self.datetime,TIME_ZONE)
    item['datetime_format']=item['datetime'].strftime("%I:%M %p").lstrip("0")
    return item
  
  def diasRegistros():
    #obtengo los dias que quiero, y a cada uno le cambio su datetime al que quiero
    fechas=HistorialChat.objects.order_by('-datetime')[:CHAT_CANT_MSJ]
    fechasArray=[]
    for fecha in fechas:
      fecha.datetime=timezone_now_cre(fecha.datetime,TIME_ZONE)
      fechasArray.append(fecha)
    ultimosDias=[registro.datetime.date() for registro in fechas]

    # quitar los repetidos
    dias=list(set(ultimosDias))

    # retornarlo ordenado
    dias.sort()

    #las pongo en un arreglo porque no puedo aplicar el reverse nativo del queryset porque hize la consulta con un slice, entonces los agrego en un arreglo para voltearlo al orden normal
    fechasArray.reverse()

    return [dias,fechasArray]