from django.shortcuts import render, get_object_or_404
from .models import Producto
from carrito.models import Venta_productos, Carrito_detalle
from django.contrib.auth.decorators import user_passes_test


def home_view(request):
    return render(request, 'home/index.html')


def listar_productos(request):
    productos= Producto.objects.all()
    return render(request, 'home/catalogo.html', {'productos': productos})


def HistorialComprasView(request):
    ventas = Venta_productos.objects.filter(id_usuario=request.user, estado_venta='pagado').order_by('-fecha_transaccion')
    return render(request, 'home/historial_compras.html', {'ventas': ventas})


def BoletaVenta(request, id):
    venta = get_object_or_404(Venta_productos, id=id)
    detalles = Carrito_detalle.objects.filter(id_venta=venta)

    return render(request, 'home/boleta_detalle.html', {
        'venta': venta,
        'detalles': detalles
    })