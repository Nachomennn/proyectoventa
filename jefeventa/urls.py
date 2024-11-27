from django.urls import path
from vendedor.views import listar_ventas, detalles_venta  # Asegúrate de importar las vistas correctamente
from . import views

app_name = 'jefeventa'

urlpatterns = [
    path('menu/', views.menu_jefe, name='menu_jefe'),
    
    # Rutas para empleados
    path('registrar_empleado/', views.registrar_empleado, name='registrar_empleado'),
    path('listar_empleados/', views.listar_empleados, name='listar_empleados'),
    path('empleado/editar/<str:run>/', views.editar_empleado, name='editar_empleado'),
    path('empleado/eliminar/<str:run>/', views.eliminar_empleado, name='eliminar_empleado'),

    # Rutas para productos
    path('agregar_producto/', views.agregar_producto, name='agregar_producto'),
    path('listar_productos/', views.listar_productos, name='listar_productos'),
    path('eliminar_producto/<str:codigo>/', views.eliminar_producto, name='eliminar_producto'),
    path('editar_producto/<str:codigo>/', views.editar_producto, name='editar_producto'),

    # Rutas para ventas
    path('ventas/detalles/<int:venta_id>/<str:origen>/', detalles_venta, name='detalles_venta'),  # Reutilizamos la vista detalles_venta
    path('ventas/listar/<str:origen>/', listar_ventas, name='listar_ventas'),
   

    # rutas para iniciar y cerrar dia
    path('iniciar_dia/', views.iniciar_dia, name='iniciar_dia'),
    path('cerrar_dia/', views.cerrar_dia, name='cerrar_dia'),
]
