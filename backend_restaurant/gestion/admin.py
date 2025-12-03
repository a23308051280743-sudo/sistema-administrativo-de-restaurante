from django.contrib import admin
from .models import Platillo, Cliente, Empleado, Pedido, Detalle_Pedido

# Para mejorar la visualización y gestión en el admin

@admin.register(Platillo)
class PlatilloAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'categoria', 'tiempo_preparacion')
    search_fields = ('nombre',)
    list_filter = ('categoria',)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'email')
    search_fields = ('nombre', 'email')

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'puesto', 'fecha_contratacion')
    search_fields = ('nombre',)
    list_filter = ('puesto',)

# Vista "inline" para que los detalles del pedido se gestionen dentro del pedido
class DetallePedidoInline(admin.TabularInline):
    model = Detalle_Pedido
    extra = 1 # Cuantos campos para añadir nuevos detalles se muestran por defecto
    autocomplete_fields = ['platillo'] # Para buscar platillos fácilmente

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'empleado', 'fecha_pedido', 'estado_pedido', 'total')
    search_fields = ('cliente__nombre', 'empleado__nombre')
    list_filter = ('fecha_pedido', 'estado_pedido')
    inlines = [DetallePedidoInline]
    readonly_fields = ('total',)

# No es necesario registrar Detalle_Pedido por separado si se usa como inline
# Pero si quieres poder gestionarlos también de forma independiente, puedes descomentar la siguiente línea:
# @admin.register(Detalle_Pedido)
# class Detalle_PedidoAdmin(admin.ModelAdmin):
#     list_display = ('id', 'pedido', 'platillo', 'cantidad', 'subtotal')
#     search_fields = ('pedido__id', 'platillo__nombre')
