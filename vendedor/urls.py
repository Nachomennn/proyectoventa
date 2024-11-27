from django.urls import path
from . import views 
from .views import exportar_ventas_excel

app_name = 'vendedor'

urlpatterns = [
    path('menu/', views.menu_vendedor, name='menu_vendedor'),
    #gestion de ventas
    path('realizar_venta/', views.realizar_venta, name='realizar_venta'),
    path('listar/', views.listar_ventas, name='listar_ventas'),
    path('detalles/<int:venta_id>/<str:origen>/', views.detalles_venta, name='detalles_venta'),
    path('exportar_ventas_excel/', exportar_ventas_excel, name='exportar_ventas_excel'),
    path('generar_pdf_venta/<int:venta_id>/', views.generar_pdf_venta, name='generar_pdf_venta'),
    path('registrar_cliente/', views.registrar_cliente, name='registrar_cliente')
    
]
