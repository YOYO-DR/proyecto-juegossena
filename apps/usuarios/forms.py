from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from apps.usuarios.models import Usuario

#creo la subclase del formulario de crear usuario para agregarle el email
class crearUsuarioForm(UserCreationForm):
    #le paso el usuario user y los fields agregando el email
    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2']

class IniciarSesionForm(AuthenticationForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for form in self.visible_fields(): # recorro cada input
          form.field.widget.attrs['class']='form-control' # les agrego la clase form-control
