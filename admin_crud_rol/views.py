from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from home.models import Producto
from home.serializers import ProductoSerializer
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_staff)
def admin_view(request):
    productos = Producto.objects.all()  # Obtener todos los productos
    usuarios = User.objects.all()  # Obtener todos los usuarios
    return render(request, 'admin/admin-index.html', {'productos': productos, 'usuarios': usuarios})

class ProductoView(APIView):
    def get(self, request):
        productos = Producto.objects.all()  # Obtener todos los productos
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Crear un nuevo producto
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        # Actualizar un producto existente
        producto = Producto.objects.get(pk=pk)
        serializer = ProductoSerializer(producto, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # "Borrar" un producto (actualizar 'activo' a False)
        producto = Producto.objects.get(pk=pk)
        producto.activo = False
        producto.save()
        return Response({"message": "Producto desactivado"}, status=status.HTTP_200_OK)
    

class UserAdminView(APIView):
    def put(self, request, pk):
            # Cambiar los permisos de un usuario a 'staff'
        user = User.objects.get(pk=pk)
        user.is_staff = not user.is_staff  # Alternar entre staff y no staff
        user.save()
        return Response({"message": "Permisos de usuario actualizados"}, status=status.HTTP_200_OK)