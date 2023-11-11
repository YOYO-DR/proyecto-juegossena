from apps.dispositivos.models import Dispositivos, Juegos
from django.db.models import Q, F, ExpressionWrapper,FloatField
from functools import reduce
from operator import and_

def obtenerGrafica(dispositivo:Dispositivos):
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
  return grafica_dispo

def obtenerParticionMayorEspacio(dispositivo:Dispositivos):
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
  return valor_mayor_discos

def potenciaDispoJuego(dispositivo:Dispositivos,juego:Juegos,valor_mayor_discos):
  data={"procesador":False,"ram":False,"grafica":[False],"disco":[False,valor_mayor_discos]}
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
  #obtener grafica de dispositivo
  grafica_com=obtenerGrafica(dispositivo)
  data['grafica']=[False,grafica_com.nombre]
  # la grafica a comparar es la que le paso en la llamada de la funcion en la cual ya verifique cual es la pontente
  juegoGrafica=juego.grafica
  if grafica_com.gb and juegoGrafica.gb:
    # si es igual, verifico la potencia de nucleos más velocidad de grafica
    if float(grafica_com.gb.gb)==float(juegoGrafica.gb.gb):
      if grafica_com.nucleos and grafica_com.velocidad:
        if (grafica_com.nucleos+grafica_com.velocidad.velocidadMhz)>=(juegoGrafica.nucleos+juegoGrafica.velocidad.velocidadMhz):
          data['grafica']=[True,grafica_com.nombre]
    # si las gb son mayores, lo paso por valido
    elif float(grafica_com.gb.gb)>float(juegoGrafica.gb.gb):
      data["grafica"]=[True,grafica_com.nombre]

  
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

  #potencia procesador, verificar los hilos y mhz
  potencia_pro_dispo=0
  if dispositivo.procesador.hilos:
    if dispositivo.procesador.mhz:
      potencia_pro_dispo=float(dispositivo.procesador.hilos)*(float(dispositivo.procesador.mhz)/1000)
    else:
      potencia_pro_dispo=float(dispositivo.procesador.hilos)
  elif dispositivo.procesador.mhz:
    potencia_pro_dispo=float(dispositivo.procesador.mhz)/1000
  
  # obtener grafica del dispositivo
  grafica_dispo=obtenerGrafica(dispositivo)
  # grafica verificaciones

  potencia_graf_dispo=0
  if grafica_dispo.nucleos:
    if grafica_dispo.velocidad:
      potencia_graf_dispo=grafica_dispo.nucleos+grafica_dispo.velocidad.velocidadMhz
    else:
      potencia_graf_dispo=grafica_dispo.nucleos
  elif grafica_dispo.velocidad:
    potencia_graf_dispo=grafica_dispo.velocidad.velocidadMhz

 # datos para realizar la busqueda
  # obtener la particion con mayor espacio y su valor
  valor_mayor_discos=obtenerParticionMayorEspacio(dispositivo)
  # puedo agregar if para preguntar si agregar o no la caraceristica según los checkboxs
  dispo_datos={"procesador":{
      "potencia":potencia_pro_dispo
    },"ram":{
      "gb":suma_rams,
    },"grafica":{
      "gb":float(grafica_dispo.gb.gb) if grafica_dispo.gb else 0,
      "potencia":potencia_graf_dispo
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
    # busco con los requisitos pedidos
    # utilizo Q para construir la consulta y guardar en el arreglo para luego pasarla al filter

    juegos=Juegos.objects

    # comienzo a realizar la consulta
    consulta=[
      Q(
        nombre__icontains=busqueda
      )
    ]

    if "ram" in datos_a_buscar:
      consulta.append(
        Q(
          ram__gb__lte=dispo_datos["ram"]["gb"]
        )
      )

    if "procesador" in datos_a_buscar:
      # utilizo el anotate para agregar un campo con la operacion de los hilos y mhz del procesador, para luego comparar con el valor que necesite
      # puedo separarlos por comas, o si abajo necesito otro campo, ejecuto de nuevo el anonotate "juegos.annotate(valor)"
      juegos=juegos.annotate(
        procesadorpotencia=ExpressionWrapper(
          F('procesador__hilos') * F('procesador__mhz') / 1000, 
          output_field=FloatField()
        )
      )
      # utilizo el ExpressionWrapper para que el resultado de la division salga como un float y poder hacer la comparacion, porque sale como un CombinedExpression, esa division
      consulta.append(
        Q(
          # lte es menor o igual, porque si es menor o igual al del dispositivo, es compatible
          procesadorpotencia__lte=dispo_datos["procesador"]["potencia"]
        )
      )

    if "grafica" in datos_a_buscar:
      juegos=juegos.annotate(
        potenciagrafica=ExpressionWrapper(
          F("grafica__nucleos")+F("grafica__velocidad__velocidadMhz"),
          output_field=FloatField()
        )
      )

      consulta.append(
        # aqui le digo que si las gb del juego son menores o iguales a la del dispositivo, verifica la potencia, si el dispositivo tiene más gb que el juego, entonces no se valida la potencia
        # si esto grafica__gb__gb__lte=dispo_datos["grafica"]["gb"] da false, osea, que la gb del juego sean menores del dispositivo, la potencia en si no se valida porque la segunda condicion de grafica__gb__gb__gt=dispo_datos["grafica"]["gb"] daria true y trae los juegos de igual forma con la grafica en valido por el OR |
        # pero si esto grafica__gb__gb__lte=dispo_datos["grafica"]["gb"] da true, se valida la potencia [potenciagrafica__lte=dispo_datos["grafica"]["potencia"]] y si o si debe dar true, porque esto [grafica__gb__gb__gt=dispo_datos["grafica"]["gb"]] daria false, pero si la potencia da false, la segunda verificacion esta false, entonces no trae nada porque no se cunplio la grafica

        Q(grafica__gb__gb__lte=dispo_datos["grafica"]["gb"]) &
          (Q(potenciagrafica__lte=dispo_datos["grafica"]["potencia"]) | 
          Q(grafica__gb__gb__gt=dispo_datos["grafica"]["gb"])) 

        # En resumen, si la condición es verdadera, se validará tanto la potencia como las GB de la gráfica. Si la condición es falsa, solo se validará que las GB de la gráfica sean mayores a dispo_datos["grafica"]["gb"].
      )
    
    # espacio
    if "espacio" in datos_a_buscar:
      consulta.append(
        Q(
          espacio__lte=dispo_datos['espacio']['gb']
        )
      )

    # Combinamos todas las condiciones con operador AND para construir la consulta final
    condicion_and = reduce(and_,consulta)

    # como converti la consulta porque esta en OR por defecto, las paso a AND (&) y condicion_and queda toda la condicion, si quisiera solo OR, paso directamente consulta al filter como .filter(*consulta)
    # el distinct() es para que los resultados sean unicos
    juegos_filtrados=juegos.filter(condicion_and).distinct()
  else:
    # busco sin requisitos pero de igual forma comparo las caracteriticas
    juegos_filtrados=Juegos.objects.filter(nombre__icontains=busqueda)
  
  # comparar juego con dispositivo
  datos_retorno=[{"juego":i.toJSON(),"comparacion":potenciaDispoJuego(dispositivo,i,valor_mayor_discos)} for i in juegos_filtrados]

  return datos_retorno

def validarJuegoDispo(dispositivo:Dispositivos,juego:Juegos):
  comparacion=potenciaDispoJuego(dispositivo,juego,obtenerParticionMayorEspacio(dispositivo))
  res=True
  for clave,valor in comparacion.items():
    if isinstance(valor,list):
      if not valor[0]:
        res=False
        break
      continue
    if not valor:
      res=False
      break
  return res