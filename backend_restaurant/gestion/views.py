
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Platillo, Cliente, Empleado, Pedido, Detalle_Pedido
from .serializers import PlatilloSerializer, ClienteSerializer, EmpleadoSerializer, PedidoSerializer, Detalle_PedidoSerializer
from .forms import PlatilloForm, ClienteForm
from decimal import Decimal

# --- Vistas para la página web del restaurante ---

def index(request):
    """Vista para la página de inicio que muestra el menú."""
    platillos = Platillo.objects.all()
    return render(request, 'gestion/index.html', {'platillos': platillos})

class ProfileView(LoginRequiredMixin, TemplateView):
    """Muestra la página de perfil del usuario autenticado."""
    template_name = 'gestion/profile.html'

# --- Vistas para el Carrito y Pedidos ---

@login_required
def add_to_cart(request, platillo_id):
    """Añade un platillo al carrito de compras."""
    platillo = get_object_or_404(Platillo, id=platillo_id)
    cart = request.session.get('cart', {})
    
    # Si el platillo ya está en el carrito, aumenta la cantidad. Si no, lo añade.
    item = cart.get(str(platillo_id))
    if item:
        item['cantidad'] += 1
    else:
        cart[str(platillo_id)] = {'nombre': platillo.nombre, 'precio': str(platillo.precio), 'cantidad': 1}
        
    request.session['cart'] = cart
    return redirect('homepage')

@login_required
def view_cart(request):
    """Muestra el contenido del carrito."""
    cart = request.session.get('cart', {})
    total_pedido = Decimal('0.00')
    items_en_carrito = []

    for platillo_id, item_data in cart.items():
        precio_total = Decimal(item_data['precio']) * item_data['cantidad']
        total_pedido += precio_total
        items_en_carrito.append({
            'id': platillo_id,
            'nombre': item_data['nombre'],
            'precio': item_data['precio'],
            'cantidad': item_data['cantidad'],
            'subtotal': precio_total
        })

    return render(request, 'gestion/cart.html', {'items': items_en_carrito, 'total': total_pedido})

@login_required
def update_cart(request, platillo_id):
    """Actualiza la cantidad de un platillo en el carrito."""
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 1))
        if cantidad > 0:
            cart = request.session.get('cart', {})
            if str(platillo_id) in cart:
                cart[str(platillo_id)]['cantidad'] = cantidad
                request.session['cart'] = cart
    return redirect('view_cart')

@login_required
def remove_from_cart(request, platillo_id):
    """Elimina un platillo del carrito."""
    cart = request.session.get('cart', {})
    if str(platillo_id) in cart:
        del cart[str(platillo_id)]
        request.session['cart'] = cart
    return redirect('view_cart')


@login_required
def create_order(request):
    """Crea un pedido en la base de datos a partir del carrito."""
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('view_cart') # Redirigir si el carrito está vacío

    # Asumiendo que el Cliente está relacionado con el User
    try:
        cliente = request.user.cliente
    except Cliente.DoesNotExist:
        # Si no existe un perfil de Cliente, podrías crearlo o mostrar un error.
        # Por ahora, mostraremos un error simple.
        return render(request, 'gestion/error.html', {'message': "No tienes un perfil de cliente asociado."})
    
    total_pedido = sum(Decimal(item['precio']) * item['cantidad'] for item in cart.values())

    pedido = Pedido.objects.create(
        cliente=cliente,
        total=total_pedido,
        estado='Pendiente'
    )

    for platillo_id, item_data in cart.items():
        platillo = get_object_or_404(Platillo, id=int(platillo_id))
        Detalle_Pedido.objects.create(
            pedido=pedido,
            platillo=platillo,
            cantidad=item_data['cantidad'],
            subtotal=Decimal(item_data['precio']) * item_data['cantidad']
        )
    
    # Limpiar el carrito
    del request.session['cart']
    
    return redirect('order_confirmation', pedido_id=pedido.id)

@login_required
def order_confirmation(request, pedido_id):
    """Muestra la confirmación de un pedido exitoso."""
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, 'gestion/order_confirmation.html', {'pedido': pedido})


# --- CRUD para Platillos (Vistas Basadas en Clases) ---

class PlatilloListView(ListView):
    model = Platillo
    template_name = 'gestion/platillo_list.html'
    context_object_name = 'platillos'

class PlatilloCreateView(CreateView):
    model = Platillo
    form_class = PlatilloForm
    template_name = 'gestion/platillo_form.html'
    success_url = "/platillos/"

class PlatilloUpdateView(UpdateView):
    model = Platillo
    form_class = PlatilloForm
    template_name = 'gestion/platillo_form.html'
    success_url = "/platillos/"

class PlatilloDeleteView(DeleteView):
    model = Platillo
    template_name = 'gestion/platillo_confirm_delete.html'
    success_url = "/platillos/"

# --- Vista para Registro de Clientes ---
class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'gestion/cliente_form.html' 
    success_url = "/"

# --- Vistas para la API (se mantienen igual) ---

class PlatilloViewSet(viewsets.ModelViewSet):
    queryset = Platillo.objects.all()
    serializer_class = PlatilloSerializer
    
    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class EmpleadoViewSet(viewsets.ModelViewSet):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

class Detalle_PedidoViewSet(viewsets.ModelViewSet):
    queryset = Detalle_Pedido.objects.all()
    serializer_class = Detalle_PedidoSerializer
