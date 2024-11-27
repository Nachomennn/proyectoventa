from django.db import models

class Cliente(models.Model):
    rut = models.CharField(max_length=12, unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    direccion = models.TextField()
    razon_social = models.CharField(max_length=100, blank=True, null=True)
    giro = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos} - {self.rut}"
