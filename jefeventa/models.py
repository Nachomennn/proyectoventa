from django.db import models

class EstadoDia(models.Model):
    estado = models.BooleanField(default=False)  # False = cerrado, True = abierto
    fecha = models.DateField(unique=True)  # Solo puede haber un estado por día

    def __str__(self):
        return f"{'Abierto' if self.estado else 'Cerrado'} - {self.fecha}"
