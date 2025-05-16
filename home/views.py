from django.shortcuts import render
from .models import Producto
from django.http import JsonResponse
import requests

# Vista principal
def home_view(request):
    return render(request, 'home/index.html')

# Vista del catálogo
def listar_productos(request):
    orden = request.GET.get('orden')
    
    if orden == 'precio_asc':
        productos = Producto.objects.all().order_by('precio')
    elif orden == 'precio_desc':
        productos = Producto.objects.all().order_by('-precio')
    elif orden == 'nombre_az':
        productos = Producto.objects.all().order_by('nombre')
    elif orden == 'nombre_za':
        productos = Producto.objects.all().order_by('-nombre')
    else:
        productos = Producto.objects.all()

    return render(request, 'home/catalogo.html', {
        'productos': productos,
        'request': request  # necesario para los {% if request.GET.orden == ... %}
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
