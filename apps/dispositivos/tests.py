from django.test import TestCase
from apps.dispositivos.models import (
  Graficas,
  GraficasGb,
  GraficasVelocidades,
  Juegos, 
  Procesadores,
  Rams,
  SistemasOperativos,TipoRam,RamsVelocidades
  )

def traerDatosDeProd():
  # graficas - esta la traigo de ultimo pq tiene las llaves foraneas de las otras dos anteriores
  graficasProd=Graficas.objects.using('production').all()
  for grafica_p in graficasProd:
      try:
        grafica,creado=Graficas.objects.using('default').get_or_create(nombre=grafica_p.nombre,nucleos=grafica_p.nucleos)
        if creado:
          if grafica_p.gb:
            gb,creado = GraficasGb.objects.using("default").get_or_create(gb=grafica_p.gb.gb)
            if not creado:
              gb.save(using='default')
            grafica.gb=gb
          if grafica_p.velocidad:
            velocidad,creado = GraficasVelocidades.objects.using("default").get_or_create(velocidadMhz=grafica_p.velocidad.velocidadMhz)
            if not creado:
              velocidad.save(using='default')
            grafica.velocidad = velocidad
          grafica.save(using='default')
      except Exception as e:
        print(f"Grafica: {grafica_p.nombre}\nError:{str(e)}")
        pass
  
  print(f"Graficas production: {Graficas.objects.using('production').count()}\nGraficas local: {Graficas.objects.using('default').count()}")
  # procesadores ----------------------------------------
  # obtener los procesadores que estan produccion traerlas a local
  for procesador_p in Procesadores.objects.using("production").all():
    try:
      Procesadores.objects.using("default").get_or_create(
        nombre=procesador_p.nombre,
        nucleos=procesador_p.nucleos,
        hilos=procesador_p.hilos,
        mhz=procesador_p.mhz,
      )
    except Exception as e:
      print(f"Procesador: {procesador_p}\nError:{str(e)}")
      pass
  
  print(
    f"Procesadores production: {Procesadores.objects.using('production').count()}\nProcesadores local: {Procesadores.objects.using('default').count()}")
  # rams
  # obtener las tipo de ram

  # crear las rams
  for ram_p in Rams.objects.using("production").all():
    try:
      datos = {
        "tipo__nombre": ram_p.tipo.nombre,
        "gb": ram_p.gb,
        "velocidad__velocidadMhz": ram_p.velocidad.velocidadMhz if ram_p.velocidad else None}

      if Rams.objects.using("default").filter(**datos).exists():
        continue
      ram=Rams(gb=ram_p.gb)
      if ram_p.tipo:
        tipo,creado=TipoRam.objects.using("default").get_or_create(nombre=ram_p.tipo.nombre)
        if not creado:
          tipo.save(using="default")
        ram.tipo=tipo
      if ram_p.velocidad:
        velocidad,creado = RamsVelocidades.objects.using("default").get_or_create(
          velocidadMhz=ram_p.velocidad.velocidadMhz)
        if not creado:
          velocidad.save(using="default")
        ram.velocidad=velocidad
      ram.save(using="default")
    except Exception as e:
      print(f'Ram: {ram_p.tipo.nombre if ram_p.tipo else ""} {ram_p.velocidad.velocidadMhz if ram_p.velocidad else ""} {ram_p.gb}\nError:{str(e)}')
      pass
  
  print(f"Rams production: {Rams.objects.using('production').count()}\nRams local: {Rams.objects.using('default').count()}")

  #  sistemas operativos
  for so_p in SistemasOperativos.objects.using("production").all():
    try:
      SistemasOperativos.objects.using("default").get_or_create(
        nombre=so_p.nombre,
      )
    except Exception as e:
      print(f"Sistema operativo: {so_p}\nError:{str(e)}")
      pass
  print(f"Sistemas operativos production: {SistemasOperativos.objects.using('production').count()}\nSistemas operativos local: {SistemasOperativos.objects.using('default').count()}")

  # juegos
  for juego_p in Juegos.objects.using("production").all():
    if Juegos.objects.using("default").filter(nombre=juego_p.nombre).exists():
      continue
    juego=Juegos(
      nombre=juego_p.nombre,
      descripcion=juego_p.descripcion,
      slug=juego_p.slug,
      urlPagina=juego_p.urlPagina,
      espacio=juego_p.espacio,
      )
    ram=Rams.objects.using("default").get(
      tipo__nombre=juego_p.ram.tipo.nombre,
      gb=juego_p.ram.gb,
      velocidad__velocidadMhz=juego_p.ram.velocidad.velocidadMhz if juego_p.ram.velocidad else None
    )
    juego.ram=ram
    procesador=Procesadores.objects.using("default").get(
      nombre=juego_p.procesador.nombre,
      nucleos=juego_p.procesador.nucleos,
      hilos=juego_p.procesador.hilos,
      mhz=juego_p.procesador.mhz,
    )
    juego.procesador=procesador

    grafica=Graficas.objects.using("default").get(
      nombre=juego_p.grafica.nombre,
    )
    juego.grafica=grafica

    sistemaOperativo=SistemasOperativos.objects.using("default").get(
      nombre=juego_p.sistemaOperativo.nombre,
    )
    juego.sistemaOperativo=sistemaOperativo
    juego.save(using="default")

  print(f"Juegos production: {Juegos.objects.using('production').count()}\nJuegos local: {Juegos.objects.using('default').count()}")
traerDatosDeProd()