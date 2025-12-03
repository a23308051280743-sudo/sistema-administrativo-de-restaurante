"""
mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
# Asegurarse de que `include` también esté importado
from django.urls import path, include 
from rest_framework import routers
# Importar las vistas de la API de la app 'gestion'
from gestion.views import (
    PlatilloViewSet, 
    ClienteViewSet, 
    EmpleadoViewSet, 
    PedidoViewSet, 
    Detalle_PedidoViewSet
)

# Crear un router para la API
router = routers.DefaultRouter()
router.register(r'platillos', PlatilloViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'empleados', EmpleadoViewSet)
router.register(r'pedidos', PedidoViewSet)
router.register(r'detalles_pedido', Detalle_PedidoViewSet)

# --- Definición de las URL principales del proyecto ---
urlpatterns = [
    # URL para el panel de administración de Django
    path('admin/', admin.site.urls),

    # URLs para la API REST (usando el router)
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # URLs para la autenticación de usuarios (login, logout, etc.)
    # Django buscará la plantilla de login en 'registration/login.html'
    path('accounts/', include('django.contrib.auth.urls')),

    # URLs de la aplicación 'gestion' (página principal, registro, etc.)
    # Esta línea ahora funcionará correctamente
    path('', include('gestion.urls')),
]
