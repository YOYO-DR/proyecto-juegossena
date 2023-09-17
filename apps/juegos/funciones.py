from apps.dispositivos.models import Dispositivos, Juegos

def potenciaDispoJuego(dispositivo:Dispositivos,juego:Juegos,grafica_com,valor_mayor_discos):
  data={"procesador":False,"ram":False,"grafica":[False,grafica_com.nombre],"disco":[False,valor_mayor_discos]}
  # procesador
  juegoPro=juego.procesador
  if dispositivo.procesador:
    dispoPro=dispositivo.procesador
    if dispoPro.mhz and dispoPro.hilos:
      if ((float(dispoPro.mhz)/1000) + float(dispoPro.hilos)) >= ((float(juegoPro.mhz)/1000) + float(juegoPro.hilos)):
        data["procesador"]=True

  # ram
  gbRamPro=0
  # el juego utiliza una foreign key
  gbRamJue=juego.ram.gb
  if dispositivo.ram:
    if not dispositivo.ram_re:
      for i in dispositivo.ram.all():
        if i.gb:
          gbRamPro+=i.gb
    else:
      for i in dispositivo.json['rams']:
        for clave,valor in i.items():
          if "tamano" in clave:
            gbRamPro+=float(valor.replace(" GB",""))
    
    data['ram']=False if gbRamPro<gbRamJue else True
  
  # grafica
  # la grafica a comparar es la que le paso en la llamada de la funcion en la cual ya verifique cual es la pontente
  juegoGrafica=juego.grafica
  if grafica_com.gb:
    if float(grafica_com.gb.gb)>=float(juegoGrafica.gb.gb):
      if grafica_com.nucleos and grafica_com.velocidad:
        if (grafica_com.nucleos+grafica_com.velocidad.velocidadMhz)>=(juegoGrafica.nucleos+juegoGrafica.velocidad.velocidadMhz):
          data['grafica']=[True,grafica_com.nombre]

  
  #disco
  if valor_mayor_discos[1]>=juego.espacio:
    data['disco']=[True,valor_mayor_discos]
  
  return data



def filtroJuegos(dispositivo:Dispositivos,busqueda:str,checkboxs:dict):
  datos_retorno=[]

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
  dispo_datos={"procesador":{
      "hilos":dispositivo.procesador.hilos,
      "mhz":dispositivo.procesador.mhz
    },"ram":{
      "gb":suma_rams,
    },"grafica":{
      "gb":float(grafica_dispo.gb.gb) if grafica_dispo.gb else 0,
      "nucleos":grafica_dispo.nucleos if grafica_dispo.nucleos else 0,
      "velocidad":grafica_dispo.velocidad.velocidadMhz if grafica_dispo.velocidad else 0
    },"espacio":{
      "gb":dispositivo.espacioGb,
      "disco":valor_mayor_discos[0] # letra de partición
    }}
  
  # guardar los nombres de las caracteristicas a buscar
  datos_a_buscar=[]
  for i in checkboxs:
    if i['checked']:
      datos_a_buscar.append(i['value'])

  # realizar consulta con Q y F

  # si requi esta, significa que si se filtra la busqueda con los requisitos, de lo contrario, si no esta, aplica la busqueda normal, aun asi mostrando si algunos datos son compatibles o no
  if "requi" in datos_a_buscar:
    # busco con los requisitos
    pass
  else:
    # busco sin requisitos pero de igual forma comparo las caracteriticas
    juegos=Juegos.objects.filter(nombre__icontains=busqueda)
  
  # comparar juego con dispositivo
  datos_retorno=[{"juego":i.toJSON(),"comparacion":potenciaDispoJuego(dispositivo,i,grafica_dispo,valor_mayor_discos)} for i in juegos]

  return datos_retorno