from django.urls import path
from . import views

app_name = 'productos'  # Define el namespace como 'productos'

urlpatterns = [
    path('agregar/', views.agregar_producto, name='agregar_producto'),
    path('listar/', views.listar_productos, name='listar_productos'),
    path('editar/<str:codigo>/', views.editar_producto, name='editar_producto'),
    path('eliminar/<str:codigo>/', views.eliminar_producto, name='eliminar_producto'),
    path('registrar_categoria/', views.registrar_categoria, name='registrar_categoria'),
    path('listar_categoria/', views.listar_categoria, name='listar_categoria'),
    path('editar_categoria/<int:id>/', views.editar_categoria, name='editar_categoria'),
    path('eliminar_categoria/<int:id>/', views.eliminar_categoria, name='eliminar_categoria'),
]