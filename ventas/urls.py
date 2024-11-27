from django.urls import path
from . import views

app_name = 'ventas'  # Espacio de nombres para las rutas de esta aplicación

urlpatterns = [
     path('venta/<int:id>/', views.venta_en_curso, name='venta_en_curso'),
 
]
