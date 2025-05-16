from django.urls import path, include
from . import views

urlpatterns = [

    path('carrito/', views.vista_carrito, name='vista_carrito'),
    path('api/carrito/', views.carrito_get_post, name='carrito_get_post'),
    path('api/carrito/eliminar/<int:detalle_id>/', views.eliminar_o_disminuir_producto, name='eliminar_o_disminuir_producto'),
    path('api/carrito/actualizar/<int:detalle_id>/', views.actualizar_cantidad_producto, name='actualizar_cantidad_producto'),
    path('api/carrito/agregar/',views.agregar_carrito, name='agregar_carrito'),
    path('api/webpay/respuesta/', views.respuesta_pago_webpay, name='resp_webpay'),
    path('api/webpay/iniciar/', views.pagar_webpy, name='pagar_webpay')
]