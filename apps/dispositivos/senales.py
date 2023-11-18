from django.db.models.signals import post_save
from django.dispatch import receiver

# señal para la creacion del objeto favorito de cada usuario cuando se cree
def activarSenales(datos):
  @receiver(post_save, sender=datos.get('usuario'))
  def crear_fav(sender, instance, created, **kwargs):
    if created:
      datos.get("favoritos").objects.create(usuario=instance)

  # Conecta la señal al modelo User
    post_save.connect(crear_fav, sender=datos.get("usuario"))
