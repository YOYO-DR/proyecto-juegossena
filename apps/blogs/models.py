from django.db import models

class Requerimientos(models.Model):
    numero=models.IntegerField(verbose_name="Numero de requerimiento")
    nombre=models.CharField(max_length=100,null=False,blank=False,verbose_name="Nombre requerimiento")
    hecho=models.BooleanField(default=False,null=False,verbose_name="Hecho")

    def __str__(self):
        return self.nombre