from apps.dispositivos.models import Dispositivos

def filtroJuegos(dispositivo:Dispositivos,busqueda:str,checkboxs:dict):
  # guardar los nombres de las caracteristicas a buscar
  datos_a_buscar=[]
  for i in checkboxs:
    if i['checked']:
      datos_a_buscar.append(i['value'])
  
  # si requi esta, significa que si se filtra la busqueda con los requisitos, de lo contrario, si no esta, aplica la busqueda normal, aun asi mostrando si algunos datos son compatibles o no
  if "requi" in datos_a_buscar:
    datos_retorno=[]
    # pregunto si se pidio la ram
    if "ram" in datos_a_buscar:
      # sumar las gb de las ram que tenga
      suma_rams=0
      # pregunto si tiene ram repetidas y asi sacar los valores del json
      if not dispositivo.ram_re:
        for i in dispositivo.ram.all():
          suma_rams+=i.gb
      else:
        for i in dispositivo.json['rams']:
          for clave,valor in i.items():
            if "tamano" in clave:
              suma_rams+=float(valor.replace(" GB",""))
    # pregunto si se pidio la grafica
    if "grafica" in datos_a_buscar:
      # obtener la grafica con más gb
      grafica_dispo=""
      #pregunto si hay mas de 2 graficas
      if len(dispositivo.grafica.all())==1:
        grafica_dispo=dispositivo.grafica.all()[0]
      else:
        # mirar que grafica es mejor
        for i in dispositivo.grafica.all():
          if i.gb:
            if grafica_dispo=="":
              grafica_dispo=i
            elif grafica_dispo.gb.gb<i.gb.gb:
              grafica_dispo=i
          elif i.velocidad:
            if grafica_dispo=="":
              grafica_dispo=i
            elif grafica_dispo.velocidad:
              if i.velocidad.velocidadMhz>grafica_dispo.velocidad.velocidadMhz:
                grafica_dispo=i
          elif i.nucleos:
            if grafica_dispo!="":
              grafica_dispo=i
            elif grafica_dispo.nucleos:
              if i.nucleos>grafica_dispo.nucleos:
                grafica_dispo=i
          else:
            # si no tiene nada de lo anterior, entonces continuo
            continue
        # si no se guardo la grafica, posiblemente sea solo una integrada entonces la guardo
        if grafica_dispo=="":
          grafica_dispo=dispositivo.grafica.all()[0]

    # pregunto si se pidio el espacio
    if "grafica" in datos_a_buscar:
      # traer los discos del json, y ver que particion tiene más espacio
      discos=[]
      for i in dispositivo.json['discos']:
        for clave,valor in i.items():
          if "disponible" in clave:
            clave=clave.replace("disponible_","")
            valor=float(valor.replace(" GB",""))
            discos.append({clave:valor})
      valor_mayor_discos=[]

      for i in discos:
        for clave,valor in i.items():
          if len(valor_mayor_discos)==0:
            valor_mayor_discos=[clave,valor]
          elif valor>valor_mayor_discos[1]:
            valor_mayor_discos=[clave,valor]

    # datos para realizar la busqueda
    # puedo agregar if para preguntar si agregar o no la caraceristica según los checkboxs
    dispo_datos={}
    # pregunto si se pide el procesador
    if "procesador" in datos_a_buscar:
      dispo_datos.setdefault({"procesador":{
        "hilos":dispositivo.procesador.hilos,
        "mhz":dispositivo.procesador.mhz
      }})

    # pregunto si se pide la ram
    if "ram" in datos_a_buscar:
      dispo_datos.setdefault({"ram":{
        "gb":suma_rams,
      }})

    # pregunto si se pide la grafica
    if "ram" in datos_a_buscar:
      dispo_datos.setdefault({"grafica":{
        "gb":float(grafica_dispo.gb.gb) if grafica_dispo.gb else 0,
        "nucleos":grafica_dispo.nucleos if grafica_dispo.nucleos else 0,
        "velocidad":grafica_dispo.velocidad.velocidadMhz if grafica_dispo.velocidad else 0
      }})

    # pregunto si se pide el espacio
    if "espacio" in datos_a_buscar:
      dispo_datos.setdefault({"espacio":{
        "gb":dispositivo.espacioGb,
        "disco":valor_mayor_discos[0] # letra de partición
      }})

   # realizar consulta con Q y F
  return datos_retorno