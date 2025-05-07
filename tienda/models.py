from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/')
    stock = models.PositiveIntegerField(default=0)
    disponible = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrito de {self.usuario.username}"

    def total(self):
        return sum(item.subtotal() for item in self.itemcarrito_set.all())

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.producto.precio * self.cantidad

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"

class Pedido(models.Model):
    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
    )

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    direccion_envio = models.TextField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    nombre_receptor = models.CharField(max_length=100, default="Sin nombre")
    email = models.EmailField(default="sinemail@ejemplo.com")
    telefono = models.CharField(max_length=20, default="", help_text="Número de WhatsApp/contacto")

    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario.username}"

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.precio_unitario * self.cantidad

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} (Pedido #{self.pedido.id})"
