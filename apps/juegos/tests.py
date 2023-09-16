# from django.test import TestCase
# import requests,os,json


# CLIENT_ID=os.environ.get('IDCLIENTE')
# SECRETO=os.environ.get('CLIENT_SECRET')

# # https://id.twitch.tv/oauth2/token?client_id=abcdefg12345&client_secret=hijklmn67890&grant_type=client_credentials

# r=requests.post("https://id.twitch.tv/oauth2/token",data={"client_id":CLIENT_ID,"client_secret":SECRETO,"grant_type":"client_credentials"})
# res=json.loads(r.text)
# print(res)

from apps.dispositivos.models import Dispositivos, Juegos
from django.db.models import Q,F
# Q para consultas más complejas
# F para operaciones con otros atributos del modelo, por ejempli, en este caso podria multiplicar la ram por la cantidadVisitas [Q("ram__mul"=F("cantidadVisitas"))]

# from django.db.models import Q, F, ExpressionWrapper, fields

# Calcula el resultado de ram * 2 y luego filtra los juegos donde el resultado sea mayor que 6
# Usamos annotate() para calcular el resultado de ram * 2 y lo etiquetamos como resultado_ram
query = Juegos.objects.annotate(resultado_ram=F('ram__gb') * 2).filter(resultado_ram__gt=6)
# Luego, aplicamos el filtro resultado_ram__gt=6 para seleccionar los juegos donde el resultado de la multiplicación sea mayor que 6.

# Imprime la consulta SQL generada
# print(query.query)
a=Dispositivos.objects.filter(nombre="pc_kenier_1",usuario_id=1).first()
ram1=a.ram.all()[0]
a.ram.add(ram1)
print(a.ram.all())