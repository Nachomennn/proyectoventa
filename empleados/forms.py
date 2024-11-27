from django import forms
from .models import Empleado

class EmpleadoForm(forms.ModelForm):
    contrasena = forms.CharField(widget=forms.PasswordInput, label="Contraseña")

    class Meta:
        model = Empleado
        fields = ['run', 'nombre', 'apellido', 'direccion', 'rol', 'contrasena']
