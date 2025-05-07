from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('productos/', views.productos_list, name='productos_list'),
    path('productos/crear/', views.producto_create, name='producto_create'),
    path('productos/<int:pk>/', views.producto_detail, name='producto_detail'),
    path('productos/<int:pk>/editar/', views.producto_update, name='producto_update'),
    path('productos/<int:pk>/eliminar/', views.producto_delete, name='producto_delete'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('checkout/', views.checkout, name='checkout'),
    path('registro/', views.registro, name='signup'),
    path('resumen/<int:pedido_id>/', views.resumen_pedido, name='resumen_pedido'),
    path('webpay/iniciar/<int:pedido_id>/', views.webpay_iniciar, name='webpay_iniciar'),
    path('webpay/retorno/', views.webpay_retorno, name='webpay_retorno'),
    path('carrito/actualizar/', views.actualizar_cantidad_carrito, name='actualizar_cantidad_carrito'),
    path('panel/', views.panel_admin, name='panel_admin'),
    path('panel/pedidos/', views.admin_pedidos, name='admin_pedidos'),
    path('panel/pedidos/<int:pedido_id>/', views.admin_pedido_detalle, name='admin_pedido_detalle'),
] 