from django import forms
from .models import Imagenes

class Formulario(forms.ModelForm):
    class Meta:
        model = Imagenes
        fields = ['archivo']