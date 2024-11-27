# ventas/models.py
from django.db import models
from productos.models import Producto
from empleados.models import Empleado
from cliente.models import Cliente

class Venta(models.Model):
    ESTADO_CHOICES = [
        ('abierta', 'Abierta'),
        ('cerrada', 'Cerrada'),
    ]
    fecha = models.DateTimeField(auto_now_add=True)
    total_neto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_con_iva = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tipo_documento = models.CharField(max_length=20, blank=True, null=True)  # Boleta o Factura
    metodo_pago = models.CharField(max_length=20, blank=True, null=True)  # Efectivo o Redbank
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, blank=True, null=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='abierta')
    vendedor = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True)



class VentaDetalle(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)  # Campo obligatorio
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Asegurarse de calcular el subtotal
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
