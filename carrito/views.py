from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Carrito
from home.models import Producto
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from .serializers import CarritoSerializer



def view_carrito(request):    
    carrito = Carrito.objects.filter(usuario=request.user)

    for item in carrito:
        item.total = item.producto.precio * item.cantidad 

    return render(request, 'carrito/carrito.html', {'carrito':carrito})

class CarritoViewSet(APIView):
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder

    def get(self, request):
        # Solo obtener los elementos del carrito para el usuario autenticado
        carrito = Carrito.objects.filter(usuario=request.user)
        carrito_serializer = CarritoSerializer(carrito, many=True)
        return Response(carrito_serializer.data)

    class CarritoViewSet(APIView):
        permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder

    def get(self, request):
        # Obtener el carrito del usuario autenticado
        carrito = Carrito.objects.filter(usuario=request.user)
        carrito_serializer = CarritoSerializer(carrito, many=True)
        return Response(carrito_serializer.data)

    def post(self, request):
        # Obtener el usuario autenticado
        user = request.user
        producto_id = request.data.get('producto')
        cantidad = request.data.get('cantidad')

        if not producto_id or not cantidad:
            return Response({"error": "Faltan datos del producto o cantidad"}, status=status.HTTP_400_BAD_REQUEST)

        # Verifica si el producto existe
        producto = Producto.objects.filter(id=producto_id).first()
        if not producto:
            return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        # Asigna el usuario autenticado al campo 'usuario' del carrito
        carrito_item, created = Carrito.objects.get_or_create(
            usuario=user,  # Aquí asignamos el usuario autenticado
            producto=producto,
            defaults={'cantidad': cantidad}
        )

        if not created:
            # Si el producto ya existe en el carrito, actualizamos la cantidad
            carrito_item.cantidad += cantidad
            carrito_item.save()

        return Response({"message": "Producto agregado al carrito", "carrito_id": carrito_item.id}, status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        # Actualizar la cantidad del carrito
        carrito_item = Carrito.objects.get(pk=pk, usuario=request.user)  # Solo el usuario puede editar su carrito
        cantidad = request.data.get('cantidad')

        if cantidad:
            carrito_item.cantidad = cantidad
            carrito_item.save()
            return Response({"message": "Cantidad del producto actualizada"}, status=status.HTTP_200_OK)
        
        return Response({"error": "No se proporcionó cantidad"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # "Borrar" el producto del carrito (actualizar 'activo' a False)
        carrito_item = Carrito.objects.get(pk=pk, usuario=request.user)
        carrito_item.delete()  # Esto eliminará el carrito del usuario
        return Response({"message": "Producto eliminado del carrito"}, status=status.HTTP_200_OK)