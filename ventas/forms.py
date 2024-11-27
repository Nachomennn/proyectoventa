# ventas/forms.py
from django import forms
from .models import Venta, VentaDetalle


class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = [
            'tipo_documento',
            'metodo_pago',
            'cliente',
            'vendedor',
        ]
        labels = {
            'tipo_documento': 'Tipo de Documento',
            'metodo_pago': 'Método de Pago',
            'cliente': 'Cliente',
            'vendedor': 'Vendedor',
        }
        widgets = {
            'tipo_documento': forms.Select(choices=[('boleta', 'Boleta'), ('factura', 'Factura')], attrs={
                'class': 'form-control',
            }),
            'metodo_pago': forms.Select(choices=[('efectivo', 'Efectivo'), ('redbank', 'Redbank')], attrs={
                'class': 'form-control',
            }),
            'cliente': forms.Select(attrs={
                'class': 'form-control',
            }),
            'vendedor': forms.Select(attrs={
                'class': 'form-control',
            }),
        }


class VentaDetalleForm(forms.ModelForm):
    class Meta:
        model = VentaDetalle
        fields = ['producto', 'cantidad']
        labels = {
            'producto': 'Producto',
            'cantidad': 'Cantidad',
        }
        widgets = {
            'producto': forms.Select(attrs={
                'class': 'form-control',
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'step': 1,
            }),
        }

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad <= 0:
            raise forms.ValidationError('La cantidad debe ser mayor a cero.')
        return cantidad
