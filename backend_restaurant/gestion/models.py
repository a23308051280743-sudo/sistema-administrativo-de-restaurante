
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# --- Modelo de Platillo ---
class Platillo(models.Model):
    CATEGORIAS = [
        ('Entrada', 'Entrada'),
        ('Plato Fuerte', 'Plato Fuerte'),
        ('Postre', 'Postre'),
        ('Bebida', 'Bebida'),
    ]
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    tiempo_preparacion = models.IntegerField(help_text="Tiempo de preparación en minutos")

    def __str__(self):
        return self.nombre

# --- Modelo de Cliente ---
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    direccion = models.TextField(blank=True) # <-- CAMPO AÑADIDO

    def __str__(self):
        return self.nombre

# --- Modelo de Empleado ---
class Empleado(models.Model):
    PUESTOS = [
        ('Mesero', 'Mesero'),
        ('Cocinero', 'Cocinero'),
        ('Cajero', 'Cajero'),
        ('Gerente', 'Gerente'),
    ]
    nombre = models.CharField(max_length=100)
    puesto = models.CharField(max_length=20, choices=PUESTOS)
    fecha_contratacion = models.DateField()

    def __str__(self):
        return f"{self.nombre} ({self.puesto})"

# --- Modelo de Pedido ---
class Pedido(models.Model):
    ESTADOS = [
        ('Recibido', 'Recibido'),
        ('En Preparacion', 'En Preparación'),
        ('Listo para Servir', 'Listo para Servir'),
        ('Servido', 'Servido'),
        ('Pagado', 'Pagado'),
        ('Cancelado', 'Cancelado'),
    ]
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    empleado = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado_pedido = models.CharField(max_length=20, choices=ESTADOS, default='Recibido')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.nombre if self.cliente else 'N/A'}"

    def recalculate_total(self):
        """Recalcula el campo 'total' sumando los subtotales de los detalles."""
        total_calculado = self.detalles.aggregate(total_sum=models.Sum('subtotal'))['total_sum'] or 0
        self.total = total_calculado
        self.save(update_fields=['total']) # Guarda solo el campo 'total' para evitar bucles de señales.

# --- Modelo de Detalle_Pedido ---
class Detalle_Pedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='detalles', on_delete=models.CASCADE)
    platillo = models.ForeignKey(Platillo, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=8, decimal_places=2, editable=False)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def __str__(self):
        return f"{self.cantidad} x {self.platillo.nombre} en Pedido #{self.pedido.id}"

    def save(self, *args, **kwargs):
        """Establece el precio y calcula el subtotal antes de guardar."""
        if not self.pk: # Solo al crear el objeto
            self.precio_unitario = self.platillo.precio
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

# --- Señales para actualizar el total del Pedido ---

@receiver(post_save, sender=Detalle_Pedido)
def update_pedido_total_on_save(sender, instance, **kwargs):
    """Actualiza el total del pedido cuando un detalle se guarda."""
    instance.pedido.recalculate_total()

@receiver(post_delete, sender=Detalle_Pedido)
def update_pedido_total_on_delete(sender, instance, **kwargs):
    """Actualiza el total del pedido cuando un detalle se elimina."""
    instance.pedido.recalculate_total()
