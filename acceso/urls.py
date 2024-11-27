from django.urls import path
from . import views

app_name = 'acceso'  # Define el espacio de nombres

urlpatterns = [
    path('', views.iniciar_sesion, name='iniciar_sesion'), 
    path('menu_jefe/', views.menu_jefe, name='menu_jefe'),
    path('menu_vendedor/', views.menu_vendedor, name='menu_vendedor'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    # Añade aquí otras rutas necesarias
]
