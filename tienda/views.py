from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Producto, Carrito, ItemCarrito, Pedido
from django.db.models import Sum
from .forms import CheckoutForm, RegistroForm
from django.contrib.auth import login
from django.urls import reverse, reverse_lazy
from django.utils.html import format_html
from django.utils.formats import localize
from django.utils import formats
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.integration_type import IntegrationType
import uuid

def catalogo(request):
    productos = Producto.objects.filter(disponible=True)
    return render(request, 'tienda/catalogo.html', {'productos': productos})

def get_or_create_carrito(request):
    if request.user.is_authenticated:
        carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    else:
        carrito_id = request.session.get('carrito_id')
        if carrito_id:
            carrito = Carrito.objects.filter(id=carrito_id, usuario__isnull=True).first()
            if not carrito:
                carrito = Carrito.objects.create()
                request.session['carrito_id'] = carrito.id
        else:
            carrito = Carrito.objects.create()
            request.session['carrito_id'] = carrito.id
    return carrito

def ver_carrito(request):
    carrito = get_or_create_carrito(request)
    items = carrito.itemcarrito_set.all()
    total = carrito.total()
    return render(request, 'tienda/carrito.html', {'items': items, 'total': total})

def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito = get_or_create_carrito(request)
    item, created = ItemCarrito.objects.get_or_create(
        carrito=carrito,
        producto=producto,
        defaults={'cantidad': 1}
    )
    if not created:
        item.cantidad += 1
        item.save()
    messages.success(request, f'Producto {producto.nombre} agregado al carrito')
    return redirect('catalogo')

def eliminar_del_carrito(request, item_id):
    carrito = get_or_create_carrito(request)
    item = get_object_or_404(ItemCarrito, id=item_id, carrito=carrito)
    item.delete()
    messages.success(request, 'Producto eliminado del carrito')
    return redirect('ver_carrito')

def checkout(request):
    carrito = get_or_create_carrito(request)
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            direccion = form.cleaned_data['direccion']
            numero_extra = form.cleaned_data['numero_extra']
            email = form.cleaned_data['email']
            direccion_completa = direccion
            if numero_extra:
                direccion_completa += f" ({numero_extra})"
            pedido = Pedido.objects.create(
                usuario=request.user if request.user.is_authenticated else None,
                direccion_envio=direccion_completa,
                total=carrito.total(),
                nombre_receptor=nombre,
                email=email
            )
            return redirect('resumen_pedido', pedido_id=pedido.id)
    else:
        form = CheckoutForm()
    return render(request, 'tienda/checkout.html', {'carrito': carrito, 'form': form})

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso!')
            return redirect('catalogo')
    else:
        form = RegistroForm()
    return render(request, 'tienda/registro.html', {'form': form})

# Home llamativa

def home(request):
    productos = Producto.objects.filter(disponible=True).order_by('-fecha_creacion')[:3]
    return render(request, 'tienda/home.html', {'productos': productos})

# Listar productos (catálogo CRUD)
def productos_list(request):
    productos = Producto.objects.all().order_by('-fecha_creacion')
    return render(request, 'tienda/productos_list.html', {'productos': productos})

# Detalle de producto
def producto_detail(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'tienda/producto_detail.html', {'producto': producto})

# Crear producto (solo staff)
@user_passes_test(lambda u: u.is_staff)
def producto_create(request):
    from django import forms
    class ProductoForm(forms.ModelForm):
        class Meta:
            model = Producto
            fields = ['nombre', 'descripcion', 'precio', 'stock', 'imagen']
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado exitosamente.')
            return redirect('productos_list')
    else:
        form = ProductoForm()
    return render(request, 'tienda/producto_form.html', {'form': form, 'accion': 'Crear'})

# Editar producto (solo staff)
@user_passes_test(lambda u: u.is_staff)
def producto_update(request, pk):
    from django import forms
    producto = get_object_or_404(Producto, pk=pk)
    class ProductoForm(forms.ModelForm):
        class Meta:
            model = Producto
            fields = ['nombre', 'descripcion', 'precio', 'stock', 'imagen']
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado exitosamente.')
            return redirect('productos_list')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'tienda/producto_form.html', {'form': form, 'accion': 'Actualizar'})

# Eliminar producto (solo staff)
@user_passes_test(lambda u: u.is_staff)
def producto_delete(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado exitosamente.')
        return redirect('productos_list')
    return render(request, 'tienda/producto_confirm_delete.html', {'producto': producto})

def webpay_iniciar(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if pedido.estado == 'completado':
        messages.error(request, 'Este pedido ya ha sido completado.')
        return redirect('catalogo')
    buy_order = str(pedido.id)
    session_id = str(uuid.uuid4())
    amount = int(pedido.total)
    return_url = request.build_absolute_uri(reverse('webpay_retorno'))
    tx = Transaction().create(
        buy_order=buy_order,
        session_id=session_id,
        amount=amount,
        return_url=return_url
    )
    return redirect(tx['url'] + '?token_ws=' + tx['token'])

def webpay_retorno(request):
    token_ws = request.GET.get('token_ws')
    tbk_token = request.GET.get('TBK_TOKEN')
    tbk_orden_compra = request.GET.get('TBK_ORDEN_COMPRA')
    tbk_id_sesion = request.GET.get('TBK_ID_SESION')

    if token_ws:
        response = Transaction().commit(token_ws)
        if response.get('status') == 'AUTHORIZED':
            pedido_id = response.get('buy_order')
            pedido = get_object_or_404(Pedido, id=pedido_id)
            pedido.estado = 'completado'
            pedido.save()
            carrito = get_or_create_carrito(request)
            carrito.itemcarrito_set.all().delete()
            if not request.user.is_authenticated:
                del request.session['carrito_id']
            messages.success(request, 'Pago realizado exitosamente.')
            return render(request, 'tienda/webpay_resultado.html', {'response': response})
        else:
            messages.error(request, 'Error al procesar el pago.')
            return render(request, 'tienda/webpay_error.html', {'mensaje': 'Error al procesar el pago.'})
    elif tbk_token:
        messages.error(request, 'Pago anulado o cancelado.')
        return render(request, 'tienda/webpay_anulado.html', {'mensaje': 'Pago anulado o cancelado.'})
    else:
        messages.error(request, 'No se recibió información de pago.')
        return render(request, 'tienda/webpay_error.html', {'mensaje': 'No se recibió información de pago.'})

def resumen_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if pedido.estado == 'completado':
        messages.error(request, 'Este pedido ya ha sido completado.')
        return redirect('catalogo')
    carrito = get_or_create_carrito(request)
    return render(request, 'tienda/resumen_pedido.html', {'pedido': pedido, 'carrito': carrito})
