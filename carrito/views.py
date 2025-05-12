from django.shortcuts import render
from .models import Carrito
from home.models import Producto
from rest_framework.response import Response
from rest_framework.decorators import api_view


def view_carrito(request):    
    carrito = Carrito.objects.filter(usuario=request.user)
    return render(request, 'carrito/carrito.html', {'carrito':carrito})