from rest_framework import viewsets
from .models import Carrito
from .serializers import CarritoSerializer
from rest_framework.response import Response
from rest_framework import status
from home.models import Producto
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

class CarritoViewSet(viewsets.ModelViewSet):
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder

    def get_queryset(self):
        # Solo obtener los elementos del carrito para el usuario autenticado
        return Carrito.objects.filter(usuario=self.request.user)

    def create(self, request, *args, **kwargs):
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
