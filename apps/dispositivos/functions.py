from .models import UrlJuegos,Telefonos,Favoritos,Favoritos_UrlJuegos,Historiales,RamsVelocidades,TipoRam,Rams,Procesadores,SistemasOperativos,GraficasGb,GraficasVelocidades,Graficas,Dispositivos

# constantes
ramMaximaVelocidad=8400

def obtenerCara(ar:list):
  g=0
  r=0
  c=0
  so=0
  st=0
  # ---------
  graficas=[]
  canGraficas=-1
  rams=[]
  canRams=-1
  cpu=[]
  canCpu=-1
  sisOp=[]
  canSis=-1
  storage=[]
  canSto=-1
  for linea in ar:
    # informacion de las graficas
    if 'Display adapter' in linea:
        # creo cada dict dentro de cada arreglo y agrego los datos, porque hay unos que no tiene todos, entonces no podria utilizar el append(dict) porque no podria saber donde hacerlo precisamente
        graficas.append({})
        canGraficas+=1
        if g==0:
          g=1
    if g!=0:
      if 'Name' in linea:
         graficas[canGraficas]['nombre']=linea.strip()[4:].strip()
         continue
      if 'Memory size' in linea:
        graficas[canGraficas]['tamano']=linea.strip()[11:].strip()
        continue
      if 'Cores' in linea:
        graficas[canGraficas]['cantidadNucleos']=linea.strip()[5:].strip()
        continue
      if 'Core clock' in linea:
        graficas[canGraficas]['velocidadNucleo']=linea.strip()[10:].strip()
        continue
      if 'Memory clock' in linea:
        graficas[canGraficas]['velocidadMemoria']=linea.strip()[12:].strip()
        g=0
        continue
    
    #informacion de las rams
    if 'DMI Memory Device' in linea:
      rams.append({})
      canRams+=1
      if r==0:
        r=1
    if r!=0:
      if 'type' in linea and 'unknown' in linea:
        del rams[canRams]
        canRams-=1
        r=0
        continue
      if 'format' in linea and 'unknown' in linea:
        del rams[canRams]
        canRams-=1
        r=0
        continue
      if 'type' in linea:
        rams[canRams]['tipo']=linea.strip()[4:].strip()
        continue
      if 'size' in linea:
        rams[canRams]['tamano']=linea.strip()[4:].strip()
        continue
      if 'speed' in linea:
        rams[canRams]['velocidad']=linea.strip()[5:].strip()
        continue
      if linea.strip()=='':
        if rams[canRams].get('tipo') and rams[canRams].get('tamano'):
          r=0
        else:
          r=0
          del rams[canRams]
          canRams-=1
        continue
          
    # informacion del procesador
    if 'Socket 1' in linea and 'ID =' in linea:
      cpu.append({})
      canCpu+=1
      if c==0:
        c=2
    if c==2:
      if 'Number of cores' in linea:
        maximoCorteC=linea.index('(')-1
        cpu[canCpu]['nucleos']=linea.strip()[15:maximoCorteC].strip()
        continue
      if 'Number of threads' in linea:
        maximoCorteH=linea.index('(')-1
        cpu[canCpu]['hilos']=linea.strip()[17:maximoCorteH].strip()
        continue
      if 'Stock frequency' in linea:
        cpu[canCpu]['velocidad']=linea.strip()[15:].strip()
        c=0
        continue

    if 'DMI Processor' in linea:
      if c==0 or c==2:
        c=1
    if c==1:
      if 'model' in linea:
        cpu[canCpu]['modelo']=linea.strip()[5:].strip()
        continue
      if 'clock speed' in linea and 'max' not in linea:
        cpu[canCpu]['velocidad']=linea.strip()[11:].strip()
        continue
      if 'max clock speed' in linea:
        cpu[canCpu]['velocidadMaxima']=linea.strip()[15:].strip()
        c=0
        continue
    
    # informacion del sistema operativo
    if 'Software' in linea:
      sisOp.append({})
      canSis+=1
      if so==0:
        so=1
    if so!=0:
      if 'Windows Version' in linea:
        # el segundo windows de la linea tiene un espacio atras, el primero que es el que no quiero, no tiene ese espacio
        bit = linea.index(' Windows')+12
        sisOp[canSis]['nombre']=linea.strip()[15:bit].strip()
        so=0
    # espacio
    if 'Drive	' in linea:
      volumeP=""
      storage.append({})
      canSto+=1
      if st==0:
        st=1
    if st!=0:
      if 'Capacity' in linea:
        storage[canSto]['capacidad']=linea.strip()[8:].strip()
        continue

      # para que no lea el tipo de bus
      if 'Type' in linea and not 'Bus' in linea:
        storage[canSto]['tipo']=linea.strip()[4:].strip()
        continue
      if 'Volume' in linea:
        if not storage[canSto].get('disponible'+volumeP):
          gbDiscoPosiciones=[linea.index(',')+1,linea.index('GBytes')] # posiciones para sacar las gb de la particion 1
          gbDisco=float(linea[gbDiscoPosiciones[0]:gbDiscoPosiciones[1]].strip()) #obtengo las gb y convierto a numero
        
          pare=[linea.index('(')+1,linea.index('percent')-1] # posiciones para cortar y sacar el porcentaje disponible
          porcentaje=float(linea[pare[0]:pare[1]]) # corto y convierto a numero
          disponible=str(round((gbDisco*(porcentaje/100)),2))+' GB' # guardo como string

          # particion
          coma=linea.strip().index(',')-2
          volumeP=linea.strip()[6:coma].strip()
          storage[canSto]['disponible_'+volumeP]=disponible
          continue
      
      if linea.strip()=="":
        st=0

  return {'graficas':graficas,'rams':rams,'procesador':cpu,'sisOpe':sisOp,'discos':storage}

def guardarCara(carate:dict):
  #guardar grafica(s)
  graficas=carate['graficas']

  #recorro las graficas y empiezo a guardar los valores
  for grafica in graficas:
    #creo el objeto de la grafica a guardar
    if not grafica.get('nombre'):
      break
    g,gCreado=Graficas.objects.get_or_create(nombre=grafica.get('nombre'))
    if grafica.get('tamano'):
      #extraigo el tamaño si existe, le quito el gb y lo convierto en numero float
      if 'MB' in grafica.get('tamano'):
        tamano=float((float(grafica.get('tamano').replace('MB','').strip()))//1000)
      else:
        tamano=float(grafica.get('tamano').replace('GB','').strip())
      # lo creo sino existe, de lo contrario solo lo obtengo
      objTama,creado = GraficasGb.objects.get_or_create(gb=tamano)
        # lo relaciono con objeto creado
      g.gb=objTama
      if creado:
        print('tamaño de grafica agregado\n')
    
    if grafica.get('velocidadNucleo'):
      #extraigo la velocidad si existe, le quito el mhz y lo convierto en numero int
      vel=int(float(grafica.get('velocidadNucleo').replace('MHz','').strip()))
      
      # lo creo sino existe, de lo contrario solo lo obtengo
      objVel,creado=GraficasVelocidades.objects.get_or_create(velocidadMhz=vel)
      if not gCreado:
        if g.velocidad:
          if not g.velocidad.velocidadMhz > objVel.velocidadMhz:
            # lo relaciono con objeto creado
            g.velocidad=objVel
        else:
          if objVel:
            g.velocidad=objVel

      if creado:
        print('velocidad de grafica agregada\n')
    
    if grafica.get('cantidadNucleos'):
      # obtengo la cantidad de nucleos y lo agrego al objeto creado
      nucleos=int(grafica.get('cantidadNucleos'))
      if nucleos != 0:
        g.nucleos=nucleos
  g.save()
  #recorro las rams y empiezo a guardar los valores
  rams=carate['rams']
  for ram in rams:
    r=Rams()
    if ram.get('velocidad'):
      vel=int(ram.get('velocidad').replace('MHz','').strip())
      if vel<ramMaximaVelocidad:
        objRam,creado=RamsVelocidades.objects.get_or_create(velocidadMhz=vel)
        r.velocidad=objRam
        if creado:
          print('Velocidad de ram agregada')
    
    if ram.get('tipo'):
      objTipo,creado=TipoRam.objects.get_or_create(nombre=ram.get('tipo'))
      r.tipo=objTipo
      if creado:
        print('Tipo de ram agregado')
    
    if ram.get('tamano'):
      tamano=int(ram.get('tamano').replace('GB','').strip())
      r.gb=tamano
      verificarExistencia=Rams.objects.filter(gb=r.gb,tipo=r.tipo,velocidad=r.velocidad).exists()
      if not verificarExistencia:
        r.save()

  procesador=carate['procesador']
  for pro in procesador:
    p=Procesadores()
    e=0
    if pro.get('modelo'):
      if Procesadores.objects.filter(nombre__iexact=pro.get('modelo')).exists():
        e=1
      if e==1:
        break
      p.nombre=pro.get('modelo')
    if pro.get('hilos'):
      hilos=int(pro.get('hilos').strip())
      p.hilos=hilos
    if pro.get('nucleos'):
      nucleosP=int(pro.get('nucleos').strip())
      p.nucleos=nucleosP
    if pro.get('velocidad'):
      vel=int(float(pro.get('velocidad').replace('MHz','').strip()))
      p.mhz=vel

    if pro.get('velocidadMaxima'):
      velM=int(float(pro.get('velocidadMaxima').replace('MHz','').strip()))
      p.mhz=velM
    p.save()

  sistema=carate['sisOpe']
  for sis in sistema:
    s=SistemasOperativos()
    if sis.get('nombre'):
      sistemaOpe=sis.get('nombre')
      if not SistemasOperativos.objects.filter(nombre__iexact=sistemaOpe).exists():
        s.nombre=sistemaOpe
        s.save()

  discos=carate['discos']
