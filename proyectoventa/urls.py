"""
URL configuration for proyectoventa project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from acceso import views as acceso_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', acceso_views.iniciar_sesion, name='inicio_sesion'),  # Página principal
    path('acceso/', include('acceso.urls', namespace='acceso')),
    path('clientes/', include('cliente.urls', namespace='cliente')), 
    path('empleados/', include('empleados.urls')),
    path('jefeventa/', include('jefeventa.urls', namespace='jefeventa')),
    path('vendedor/', include('vendedor.urls', namespace='vendedor')),
    path('ventas/', include('ventas.urls')),
    path('productos/', include('productos.urls', namespace='productos')),
]

# Configuración para servir archivos multimedia
if settings.DEBUG:  # Solo en modo de desarrollo
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
