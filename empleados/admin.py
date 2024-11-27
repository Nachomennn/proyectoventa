from django.contrib import admin
from .models import Empleado

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'run', 'nombre', 'apellido', 'rol','contrasena')
    search_fields = ('usuario', 'run', 'nombre', 'apellido')
    list_filter = ('rol',)
