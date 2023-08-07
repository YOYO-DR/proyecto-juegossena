from django.db import models
from apps.usuarios.models import Usuario

class Telefonos(models.Model):
    numeroTelefono=models.CharField(max_length=20,null=False, blank=False,verbose_name="Numero de telefono")
    usuario=models.ForeignKey(Usuario,on_delete=models.CASCADE,null=False,blank=False, verbose_name="Usuario")

    class Meta:
        verbose_name = 'Telefono'
        verbose_name_plural = 'Telefonos'
    
    def __str__(self):
        return self.usuario.username

class Favoritos(models.Model):
    usuario=models.ForeignKey(Usuario,on_delete=models.CASCADE,null=False,blank=False,verbose_name="Usuario")

    class Meta:
        verbose_name = 'Favorito'
        verbose_name_plural = 'Favoritos'
    
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
    
    def __Str__(self):
        return self.nombre

class Rams(models.Model):
    gb=models.IntegerField(null=False, blank=False,verbose_name="Espacio gb")
    tipo=models.ForeignKey(TipoRam, on_delete=models.CASCADE ,null=False, blank=False,verbose_name="Tipo ram")
    velocidad = models.ForeignKey(RamsVelocidades,on_delete=models.CASCADE,null=True,blank=True,verbose_name="Velocidad")

    class Meta:
        verbose_name = 'Ram'
        verbose_name_plural = 'Rams'
    
    def __str__(self):
        return f'{str(self.gb)} GB - {self.tipo.nombre} - {str(self.velocidad.velocidadMhz)} Mhz'

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

class Juegos(models.Model):
    nombre=models.CharField(max_length=200,unique=True,verbose_name="Nombre")
    urlPagina=models.URLField(verbose_name="Url pagina")
    ram=models.ForeignKey(Rams,on_delete=models.SET_NULL,null=True,verbose_name="Ram")
    procesador=models.ForeignKey(Procesadores,on_delete=models.SET_NULL,null=True,verbose_name="Procesador")
    grafica=models.ForeignKey(Graficas,on_delete=models.SET_NULL,null=True,verbose_name="Grafica")
    espacio=models.IntegerField(verbose_name="Espacio necesario")
    promedioPotencia=models.IntegerField(verbose_name="Promedio potencia",null=True,blank=True)

    def __str__(self):
        return self.nombre

class Dispositivos(models.Model):
    espacioGb = models.IntegerField(null=True,blank=True,verbose_name="Espacio gb")
    nombre = models.CharField(max_length=200,null=True,blank=True,unique=True,verbose_name="Nombre")
    usuario=models.ForeignKey(Usuario,on_delete=models.CASCADE,null=False,blank=False,verbose_name="Usuario")
    procesador=models.ForeignKey(Procesadores,on_delete=models.SET_NULL,null=True,blank=True,verbose_name="Procesador")
    # porque puede tener varias rams
    ram=models.ManyToManyField(Rams,verbose_name="Ram")
    # porque puede tener varias graficas
    grafica=models.ManyToManyField(Graficas,verbose_name="Grafica")
    sistemaOperativo=models.ForeignKey(SistemasOperativos,on_delete=models.SET_NULL,null=True,blank=True,verbose_name="Sistema operativo") 
    promedioPotencia=models.IntegerField(null=True,blank=True,verbose_name="Promedio potencia")

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

class Favoritos_UrlJuegos(models.Model):
    favorito = models.ForeignKey(Favoritos,on_delete=models.CASCADE,null=False,blank=False,verbose_name="Favorito")
    juego = models.ForeignKey(Juegos,on_delete=models.CASCADE,null=False,blank=False,verbose_name="Juego")

    class Meta:
        verbose_name = 'Favorito_juego'
        verbose_name_plural = 'Favoritos_juegos'
    def __str__(self):
        return self.juego.nombre