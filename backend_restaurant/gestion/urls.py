from django.urls import path
from .views import (
    index,
    PlatilloListView,
    PlatilloCreateView,
    PlatilloUpdateView,
    PlatilloDeleteView,
    ClienteCreateView,
    ProfileView,
    add_to_cart,
    view_cart,
    update_cart,        # <-- Importar la nueva vista
    remove_from_cart,   # <-- Importar la nueva vista
    create_order,
    order_confirmation
)

urlpatterns = [
    # --- URLs de la Tienda y Perfil ---
    path('', index, name='homepage'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('registro/', ClienteCreateView.as_view(), name='cliente_registro'),

    # --- URLs del Carrito y Proceso de Pedido ---
    path('add-to-cart/<int:platillo_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('cart/update/<int:platillo_id>/', update_cart, name='update_cart'),
    path('cart/remove/<int:platillo_id>/', remove_from_cart, name='remove_from_cart'),
    path('create-order/', create_order, name='create_order'),
    path('order-confirmation/<int:pedido_id>/', order_confirmation, name='order_confirmation'),

    # --- URLs para el CRUD de Platillos (Administración) ---
    path('platillos/', PlatilloListView.as_view(), name='platillo_list'),
    path('platillos/nuevo/', PlatilloCreateView.as_view(), name='platillo_create'),
    path('platillos/<int:pk>/editar/', PlatilloUpdateView.as_view(), name='platillo_update'),
    path('platillos/<int:pk>/eliminar/', PlatilloDeleteView.as_view(), name='platillo_delete'),
]
