from django.shortcuts import render, get_object_or_404
from .models import Venta

def venta_en_curso(request, id):
    venta = get_object_or_404(Venta, id=id)
    detalles = venta.detalles.all()  # Si usas related_name='detalles'

    return render(request, 'ventas/venta_en_curso.html', {
        'venta': venta,
        'detalles': detalles,
    })
