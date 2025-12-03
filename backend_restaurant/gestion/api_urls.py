from rest_framework.routers import SimpleRouter
from .views import PlatilloViewSet, ClienteViewSet, EmpleadoViewSet, PedidoViewSet, Detalle_PedidoViewSet

# --- Rutas para la API ---
router = SimpleRouter()
router.register(r'platillos', PlatilloViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'empleados', EmpleadoViewSet)
router.register(r'pedidos', PedidoViewSet)
router.register(r'detalles_pedido', Detalle_PedidoViewSet)

urlpatterns = router.urls
