from django.contrib import admin
from .models import Producto, Carrito, ItemCarrito, Pedido

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock', 'disponible')
    list_filter = ('disponible',)
    search_fields = ('nombre', 'descripcion')

@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha_creacion')
    search_fields = ('usuario__username',)

@admin.register(ItemCarrito)
class ItemCarritoAdmin(admin.ModelAdmin):
    list_display = ('carrito', 'producto', 'cantidad')
    list_filter = ('carrito__usuario',)

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'estado', 'total', 'fecha_creacion')
    list_filter = ('estado',)
    search_fields = ('usuario__username',)
