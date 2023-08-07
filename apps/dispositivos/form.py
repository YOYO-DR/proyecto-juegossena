from django import forms

from apps.dispositivos.models import Dispositivos


class DispositivosForm(forms.ModelForm):
    class Meta:
        model=Dispositivos
        fields="__all__"
        exclude=['usuario',"promedioPotencia"]
