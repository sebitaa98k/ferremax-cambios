from django.shortcuts import render
from .models import Producto


def home_view(request):
    return render(request, 'home/index.html')


def listar_productos(request):
    productos= Producto.objects.all()
    return render(request, 'home/catalogo.html', {'productos': productos})
