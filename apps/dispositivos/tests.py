from django.test import TestCase
from apps.dispositivos.models import Graficas,GraficasGb,GraficasVelocidades

def traerDatosDeProd():
  # obtener las graficas que estan produccion traerlas a local
  graficasvelocidadesProd=GraficasVelocidades.objects.using('production').all()
  for graficavelocidad in graficasvelocidadesProd:
      try:
        graficavelocidad.save(using='default')
      except Exception as e:
        print(e)
        pass

  # graficas gb
  graficasgbProd=GraficasGb.objects.using('production').all()
  for graficagb in graficasgbProd:
      try:
        graficagb.save(using='default')
      except Exception as e:
        print(e)
        pass

  # graficas - esta la traigo de ultimo pq tiene las llaves foraneas de las otras dos anteriores
  graficasProd=Graficas.objects.using('production').all()
  for grafica in graficasProd:
      try:
        datos={}
        if grafica.nombre:
          datos['nombre']=grafica.nombre
        if grafica.nucleos:
          datos['nucleos']=grafica.nucleos
        if grafica.gb:
          datos['gb__gb']=grafica.gb.gb
        if grafica.velocidad:
          if grafica.velocidad.velocidadMhz:
            datos['velocidad__velocidadMhz']=grafica.velocidad.velocidadMhz
        grafica_v=Graficas.objects.get_or_create(**datos)
        grafica.save(using='default')
      except Exception as e:
        print(e)
        pass

traerDatosDeProd()