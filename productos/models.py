from django.db import models
import os

class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'categoria'

class Producto(models.Model):
    codigoBarra = models.CharField(primary_key=True, max_length=50)
    nombre = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    descripcion = models.TextField(max_length=300)
    estado = models.BooleanField(default=True)  # 0: Activo, 1: Inactivo
    foto = models.ImageField(upload_to='productos/', blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.nombre} - {self.categoria.nombre if self.categoria else "Sin categoría"}'

    def delete(self, *args, **kwargs):
        if self.foto:
            if os.path.isfile(self.foto.path):
                os.remove(self.foto.path)
        super().delete(*args, **kwargs)

    class Meta:
        db_table = 'producto'
