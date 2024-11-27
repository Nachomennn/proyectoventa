from django.contrib import admin
from .models import Producto, Categoria

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigoBarra', 'nombre', 'categoria', 'precio', 'stock', 'estado')
    search_fields = ('codigoBarra', 'nombre')
    list_filter = ('categoria', 'estado')
