from django.db import models
from django.contrib.auth.hashers import make_password

class Empleado(models.Model):
    usuario = models.CharField(max_length=50)
    contrasena = models.CharField(max_length=128)  # Almacena contraseñas de forma segura
    run = models.CharField(max_length=12, unique=True)  # Campo único para el RUN
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    
    ROL_CHOICES = [
        ('jefe', 'Jefe de Ventas'),
        ('vendedor', 'Vendedor'),
    ]
    rol = models.CharField(max_length=10, choices=ROL_CHOICES)

    def save(self, *args, **kwargs):
        # Encriptar la contraseña solo si es nueva o si fue modificada
        if not self.pk or not self.contrasena.startswith('pbkdf2_'):  # Verifica si la contraseña está encriptada
            self.contrasena = make_password(self.contrasena)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.usuario}"
