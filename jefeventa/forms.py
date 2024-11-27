from django import forms
from empleados.models import Empleado  # Asegúrate de usar la ruta correcta

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['run', 'nombre', 'apellido', 'direccion', 'rol', 'contrasena']
        widgets = {
            'contrasena': forms.PasswordInput(),
        }
