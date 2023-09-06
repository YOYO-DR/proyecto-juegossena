import os
from django.db import models
from django.forms import model_to_dict
from apps.funciones_gen import redondear
from apps.usuarios.models import Usuario
from config.settings import MEDIA_URL,STATIC_URL, STATIC_URL_AZURE
from django.db.models.signals import post_save
from django.dispatch import receiver

class Telefonos(models.Model):
    numeroTelefono=models.CharField(max_length=20,null=False, blank=False,verbose_name="Numero de telefono")
    usuario=models.ForeignKey(Usuario,on_delete=models.CASCADE,null=False,blank=False, verbose_name="Usuario")

    class Meta:
        verbose_name = 'Telefono'
        verbose_name_plural = 'Telefonos'
    
    def __str__(self):
        return self.usuario.username

class Historiales(models.Model):
    busqueda = models.CharField(max_length=100,null=False,blank=False,verbose_name="Busqueda")
    fechaBusqueda=models.DateField(auto_now_add=True,verbose_name="Fecha de busqueda")
    usuario=models.ForeignKey(Usuario,on_delete=models.CASCADE,null=False,blank=False,verbose_name="Usuario")

    class Meta:
        verbose_name = 'Historial'
        verbose_name_plural = 'Historiales'
    
    def __str__(self):
        return self.usuario.username

class RamsVelocidades(models.Model):
    velocidadMhz = models.IntegerField(null=False, blank=False,verbose_name="Velocidad Mhz")

    class Meta:
        verbose_name = 'Ram Velocidad'
        verbose_name_plural = 'Rams Velocidades'
    
    def __str__(self):
        return str(self.velocidadMhz) + ' Mhz'

class TipoRam(models.Model):
    nombre=models.CharField(max_length=10,null=False, blank=False,verbose_name="Tipo ram")

    class Meta:
        verbose_name = 'Tipo ram'
        verbose_name_plural = 'Tipos rams'
    
    def __str__(self):
        return self.nombre

class Rams(models.Model):
    gb=models.IntegerField(null=False, blank=False,verbose_name="Espacio gb")
    tipo=models.ForeignKey(TipoRam, on_delete=models.CASCADE ,null=False, blank=False,verbose_name="Tipo ram")
    velocidad = models.ForeignKey(RamsVelocidades,on_delete=models.CASCADE,null=True,blank=True,verbose_name="Velocidad")

    class Meta:
        verbose_name = 'Ram'
        verbose_name_plural = 'Rams'
    
    def __str__(self):
        if self.velocidad:
          return f'{str(self.gb)} GB - {self.tipo.nombre} - {str(self.velocidad.velocidadMhz)} Mhz'

        return f'{str(self.gb)} GB - {self.tipo.nombre}'
    def toJSON(self):
        item=model_to_dict(self,exclude=['tipo','velocidad'])
        item["tipo"]=self.tipo.nombre if self.tipo else None
        item["velocidad"]=self.velocidad.velocidadMhz if self.velocidad else None
        return item

class Procesadores(models.Model):
    nombre = models.CharField(max_length=100,null=False, blank=False,verbose_name="Nombre")
    nucleos=models.IntegerField(null=True, blank=True,verbose_name="Nucleos")
    hilos=models.IntegerField(null=True, blank=True,verbose_name="Hilos")
    mhz=models.IntegerField(null=True, blank=True,verbose_name="Potencia Mhz")

    class Meta:
        verbose_name = 'Procesador'
        verbose_name_plural = 'Procesadores'
    
    def __str__(self):
        return self.nombre
    
    def toJSON(self):
        return model_to_dict(self)

class SistemasOperativos(models.Model):
    nombre = models.CharField(max_length=100,null=False, blank=False,unique=True,verbose_name="Nombre")

    class Meta:
        verbose_name = 'Sistema Operativo'
        verbose_name_plural = 'Sistema Operativos'
    
    def __str__(self):
        return self.nombre

class GraficasGb(models.Model):
    gb=models.DecimalField(max_digits=9,decimal_places=2,null=False, blank=False,verbose_name="Espacio gb")

    class Meta:
        verbose_name = 'Grafica gb'
        verbose_name_plural = 'Graficas gb'
    
    def __str__(self):
        return str(self.gb)

class GraficasVelocidades(models.Model):
    velocidadMhz=models.IntegerField(null=False, blank=False,verbose_name="Velocidad mhz")

    class Meta:
        verbose_name = 'Grafica velocidad'
        verbose_name_plural = 'Graficas velocidades'
    
    def __str__(self):
        return str(self.velocidadMhz)

class Graficas(models.Model):
    nombre = models.CharField(max_length=100,null=False, blank=False,verbose_name="Nombre")
    nucleos=models.IntegerField(null=True, blank=True,verbose_name="Nucleos")
    gb=models.ForeignKey(GraficasGb,on_delete=models.CASCADE,null=True, blank=True,verbose_name="Espacio gb")
    velocidad=models.ForeignKey(GraficasVelocidades,on_delete=models.CASCADE,null=True,blank=True,verbose_name="Velocidad")

    class Meta:
        verbose_name = 'Grafica'
        verbose_name_plural = 'Graficas'
    
    def __str__(self):
        return self.nombre
    
    def toJSON(self):
        item = model_to_dict(self,exclude=['gb','velocidad'])
        item['gb']=float(self.gb.gb) if self.gb else None
        item['velocidad']=self.velocidad.velocidadMhz if self.velocidad else None
        return item

class Juegos(models.Model):
    nombre=models.CharField(max_length=200,unique=True,verbose_name="Nombre")
    descripcion=models.CharField(max_length=500,verbose_name="Descripción",null=False,blank=False)
    slug=models.CharField(max_length=200,unique=True,verbose_name="Slug",default="juego")
    urlPagina=models.URLField(verbose_name="Url pagina")
    ram=models.ForeignKey(Rams,on_delete=models.SET_NULL,null=True,verbose_name="Ram")
    procesador=models.ForeignKey(Procesadores,on_delete=models.SET_NULL,null=True,verbose_name="Procesador")
    grafica=models.ForeignKey(Graficas,on_delete=models.SET_NULL,null=True,verbose_name="Grafica")
    espacio=models.IntegerField(verbose_name="Espacio necesario en gb")
    cantidadVisitas=models.IntegerField(verbose_name="Cantidad visitas",default=0)
    imagen=models.ImageField(upload_to=f'{MEDIA_URL}imagen/%Y/%m/' if 'WEBSITE_HOSTNAME' in os.environ else 'imagen/%Y/%m/',null=True,blank=True, verbose_name='Imagen juego')
    sistemaOperativo=models.ForeignKey(SistemasOperativos,on_delete=models.SET_NULL,null=True,blank=True,verbose_name="Sistema operativo")

    def __str__(self):
        return self.nombre
    
    def get_imagen(self):
        if self.imagen:
            return self.imagen.url
        return f'{STATIC_URL_AZURE}media/img/empty.png' if 'WEBSITE_HOSTNAME' in os.environ else f'{STATIC_URL}media/img/empty.png'
    
    def toJSON(self):
        item=model_to_dict(self)
        item['imagen']=self.get_imagen()
        item['procesador']=self.procesador.toJSON()
        item['grafica']=self.grafica.toJSON()
        item['ram']=self.ram.toJSON()
        return item
    
    def requisitos(self):
        return {
            'ram':f"{self.ram.gb} GB",
            'procesador':self.procesador.nombre,
            'grafica':f'{self.grafica.nombre} - {redondear(self.grafica.gb.gb,2)} GB',
            'espaciore':f'{self.espacio} GB',
            'so':self.sistemaOperativo.nombre
        }

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
      # para que cuando se guarde, se genere el slug para su vista
      self.slug=(self.nombre.replace(" ","-")).lower()
      return super(Juegos,self).save()
    class Meta:
        verbose_name="Juego"
        verbose_name_plural="Juegos"

class Dispositivos(models.Model):
    espacioGb = models.IntegerField(null=True,blank=True,verbose_name="Espacio gb")
    nombre = models.CharField(max_length=200,null=True,blank=True,verbose_name="Nombre")
    usuario=models.ForeignKey(Usuario,on_delete=models.CASCADE,null=False,blank=False,verbose_name="Usuario")
    procesador=models.ForeignKey(Procesadores,on_delete=models.SET_NULL,null=True,blank=True,verbose_name="Procesador")
    # porque puede tener varias rams
    ram=models.ManyToManyField(Rams,verbose_name="Ram")
    # porque puede tener varias graficas
    grafica=models.ManyToManyField(Graficas,verbose_name="Grafica")
    sistemaOperativo=models.ForeignKey(SistemasOperativos,on_delete=models.SET_NULL,null=True,blank=True,verbose_name="Sistema operativo") 
    json=models.JSONField(null=True,blank=True,verbose_name="Json presentación")

    class Meta:
        verbose_name = 'Dispositivo'
        verbose_name_plural = 'Dispositivos'
    
    def __str__(self):
        try:
          valor=self.usuario.username + " - " + self.nombre
          return valor
        except Exception as e:
          pass
        return str(self.id)
    
    def limpiar(self):
        self.ram.clear()
        self.grafica.clear()

    def toJSON(self):
        item=model_to_dict(self,exclude=['usuario',"ram","grafica"])
        if self.ram:
          ram=[]
          for i in self.ram.all():
            ram.append(i.toJSON())
          item['ram']=ram
        if self.grafica:
            grafica=[]
            for i in self.grafica.all():
                grafica.append(i.toJSON())
            item['grafica']=grafica
        item['procesador']=self.procesador.toJSON()
        item['sistemaOperativo']=self.sistemaOperativo.nombre
        return item

class Favoritos(models.Model):
    usuario=models.OneToOneField(Usuario,on_delete=models.CASCADE,null=False,blank=False,verbose_name="Usuario")
    juegos=models.ManyToManyField(Juegos,blank=True)

    class Meta:
        verbose_name = 'Favorito'
        verbose_name_plural = 'Favoritos'
    
    def __str__(self):
        return self.usuario.username

# señal para la creacion del objeto favorito de cada usuario cuando se cree
@receiver(post_save, sender=Usuario)
def crear_fav(sender, instance, created, **kwargs):
  if created:
    Favoritos.objects.create(usuario=instance)

# Conecta la señal al modelo User
post_save.connect(crear_fav, sender=Usuario)

class ImagenesJuego(models.Model):
  juego=models.ForeignKey(Juegos,on_delete=models.CASCADE,null=False, blank=False)
  imagen=models.ImageField(upload_to=f'{MEDIA_URL}imagenes_juegos/%Y/%m/' if 'WEBSITE_HOSTNAME' in os.environ else 'imagenes_juegos/%Y/%m/',null=True,blank=True, verbose_name='Imagen')

  def __str__(self):
      return self.juego.nombre
  
  def get_imagen(self):
      if self.imagen:
        return self.imagen.url
      return f'{STATIC_URL_AZURE}media/img/empty.png' if 'WEBSITE_HOSTNAME' in os.environ else f'{STATIC_URL}media/img/empty.png'
  
  def toJSON(self):
      item=model_to_dict(self)
      item['imagen']=self.get_imagen()
      return item