from django.db import models
from apps.usuarios.models import Usuario

class UrlJuegos(models.Model):
    url = models.TextField(null=False, blank=False)
    nombreJuego = models.CharField(max_length=100,null=False,blank=False)

    class Meta:
        verbose_name = 'Url Juego'
        verbose_name_plural = 'Url Juegos'
    
    def __str__(self):
        return self.nombreJuego

class Telefonos(models.Model):
    numeroTelefono=models.CharField(max_length=20,null=False, blank=False)
    usuario=models.ForeignKey(Usuario,on_delete=models.CASCADE,null=False,blank=False)

    class Meta:
        verbose_name = 'Telefono'
        verbose_name_plural = 'Telefonos'
    
    def __str__(self):
        return self.usuario.username

class Favoritos(models.Model):
    usuario=models.ForeignKey(Usuario,on_delete=models.CASCADE,null=False,blank=False)

    class Meta:
        verbose_name = 'Favorito'
        verbose_name_plural = 'Favoritos'
    
    def __str__(self):
        return self.usuario.username

class Favoritos_UrlJuegos(models.Model):
    favorito = models.ForeignKey(Favoritos,on_delete=models.CASCADE,null=False,blank=False)
    urlJuego = models.ForeignKey(UrlJuegos,on_delete=models.CASCADE,null=False,blank=False)

    class Meta:
        verbose_name = 'Favorito_urlJuego'
        verbose_name_plural = 'Favoritos_urlJuegos'
    def __str__(self):
        return self.urlJuego.nombreJuego

class Historiales(models.Model):
    busqueda = models.CharField(max_length=100,null=False,blank=False)
    fechaBusqueda=models.DateField(auto_now_add=True)
    usuario=models.ForeignKey(Usuario,on_delete=models.CASCADE,null=False,blank=False)

    class Meta:
        verbose_name = 'Historial'
        verbose_name_plural = 'Historiales'
    
    def __str__(self):
        return self.usuario.username

class RamsVelocidades(models.Model):
    velocidadMhz = models.IntegerField(null=False, blank=False)

    class Meta:
        verbose_name = 'Ram Velocidad'
        verbose_name_plural = 'Rams Velocidades'
    
    def __str__(self):
        return str(self.velocidadMhz) + ' Mhz'

class TipoRam(models.Model):
    nombre=models.CharField(max_length=10,null=False, blank=False)

    class Meta:
        verbose_name = 'Tipo ram'
        verbose_name_plural = 'Tipos rams'
    
    def __Str__(self):
        return self.nombre

class Rams(models.Model):
    gb=models.IntegerField(null=False, blank=False)
    tipo=models.ForeignKey(TipoRam, on_delete=models.CASCADE ,null=False, blank=False)
    velocidad = models.ForeignKey(RamsVelocidades,on_delete=models.CASCADE,null=True,blank=True)

    class Meta:
        verbose_name = 'Ram'
        verbose_name_plural = 'Rams'
    
    def __str__(self):
        return f'{str(self.gb)} GB - {self.tipo.nombre} - {str(self.velocidad.velocidadMhz)} Mhz'

class Procesadores(models.Model):
    nombre = models.CharField(max_length=100,null=False, blank=False)
    nucleos=models.IntegerField(null=True, blank=True)
    hilos=models.IntegerField(null=True, blank=True)
    mhz=models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Procesador'
        verbose_name_plural = 'Procesadores'
    
    def __str__(self):
        return self.nombre

class SistemasOperativos(models.Model):
    nombre = models.CharField(max_length=100,null=False, blank=False,unique=True)

    class Meta:
        verbose_name = 'Sistema Operativo'
        verbose_name_plural = 'Sistema Operativos'
    
    def __str__(self):
        return self.nombre

class GraficasGb(models.Model):
    gb=models.DecimalField(max_digits=9,decimal_places=2,null=False, blank=False)

    class Meta:
        verbose_name = 'Grafica gb'
        verbose_name_plural = 'Graficas gb'
    
    def __str__(self):
        return str(self.gb)

class GraficasVelocidades(models.Model):
    velocidadMhz=models.IntegerField(null=False, blank=False)

    class Meta:
        verbose_name = 'Grafica velocidad'
        verbose_name_plural = 'Graficas velocidades'
    
    def __str__(self):
        return str(self.velocidadMhz)

class Graficas(models.Model):
    nombre = models.CharField(max_length=100,null=False, blank=False)
    nucleos=models.IntegerField(null=True, blank=True)
    gb=models.ForeignKey(GraficasGb,on_delete=models.CASCADE,null=True, blank=True)
    velocidad=models.ForeignKey(GraficasVelocidades,on_delete=models.CASCADE,null=True,blank=True)

    class Meta:
        verbose_name = 'Grafica'
        verbose_name_plural = 'Graficas'
    
    def __str__(self):
        return self.nombre

class Dispositivos(models.Model):
    espacioGb = models.IntegerField(null=False,blank=False)
    nombre = models.CharField(max_length=200,null=True,blank=True)
    usuario=models.ForeignKey(Usuario,on_delete=models.CASCADE,null=False,blank=False)
    procesador=models.ForeignKey(Procesadores,on_delete=models.CASCADE,null=False,blank=False)
    ram=models.ForeignKey(Rams,on_delete=models.CASCADE,null=False,blank=False)
    grafica=models.ForeignKey(Graficas,on_delete=models.CASCADE,null=False,blank=False)
    sistemaOperativo=models.ForeignKey(SistemasOperativos,on_delete=models.CASCADE,null=False,blank=False)

    class Meta:
        verbose_name = 'Dispositivo'
        verbose_name_plural = 'Dispositivos'
    
    def __str__(self):
        return self.usuario.username