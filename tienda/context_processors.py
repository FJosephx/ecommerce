from .models import Carrito

def carrito(request):
    if request.user.is_authenticated:
        carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
        return {'carrito': carrito}
    else:
        carrito_id = request.session.get('carrito_id')
        if carrito_id:
            carrito = Carrito.objects.filter(id=carrito_id, usuario__isnull=True).first()
            if carrito:
                return {'carrito': carrito}
        return {'carrito': None} 