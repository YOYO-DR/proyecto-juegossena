from .models import Usuario

usuario=Usuario.objects.get(pk=1)
usuario.is_active=True
usuario.save()