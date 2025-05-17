from django.shortcuts import render, get_object_or_404
from .models import Producto
from carrito.models import Venta_productos, Carrito_detalle
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
import requests


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


def listar_productos(request):
    orden = request.GET.get('orden')
    buscar = request.GET.get('buscar')

    productos = Producto.objects.all()

    if buscar:
        productos = productos.filter(nombre__icontains=buscar)

    if orden == 'precio_asc':
        productos = productos.order_by('precio')
    elif orden == 'precio_desc':
        productos = productos.order_by('-precio')
    elif orden == 'nombre_az':
        productos = productos.order_by('nombre')
    elif orden == 'nombre_za':
        productos = productos.order_by('-nombre')

    return render(request, 'home/catalogo.html', {
        'productos': productos,
        'request': request
    })

def test_404_view(request):
    return render(request, '404.html', status=404)

# Vista para obtener la tasa de cambio
FASTFOREX_API_KEY = 'b9524382db-a7a864c2dc-swbh8a' 
def obtener_tasa(request):
    base = request.GET.get('base', 'CLP')
    target = request.GET.get('target', 'USD')

    url = f"https://api.fastforex.io/fetch-one?from={base}&to={target}&api_key={FASTFOREX_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        tasa = data['result'][target]
        return JsonResponse({'tasa': tasa})
    else:
        return JsonResponse({'error': 'No se pudo obtener la tasa'}, status=500)
