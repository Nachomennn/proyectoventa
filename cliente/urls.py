from django.urls import path
from vendedor.views import registrar_cliente, listar_clientes, editar_cliente, eliminar_cliente

app_name = 'cliente'

urlpatterns = [
    path('registrar/', registrar_cliente, name='registrar_cliente'),
    path('listar_cliente/', listar_clientes, name='listar_cliente'),
    path('editar/<int:id>/', editar_cliente, name='editar_cliente'),
    path('eliminar/<int:id_cliente>/', eliminar_cliente, name='eliminar_cliente'),
]
