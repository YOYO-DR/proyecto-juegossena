from django.db import models
from django.forms import model_to_dict

# Create your models here.
class PreguntaAyuda(models.Model):
  pregunta=models.CharField(max_length=200,null=False,blank=False,unique=True,verbose_name="Pregunta")
  respuesta=models.TextField(null=False,blank=False,verbose_name="Respuesta")

  def __str__(self):
    return self.pregunta

  def toJSON(self):
    return model_to_dict(self)
  
  class Meta:
    verbose_name="Pregunta ayuda"
    verbose_name_plural="Preguntas ayuda"