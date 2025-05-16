from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.http import JsonResponse
from home.models import Producto
from carrito.models import Venta_productos
from home.serializers import ProductoSerializer
from django.contrib.auth.decorators import user_passes_test, login_required
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

@user_passes_test(lambda u: u.is_staff)
def admin_view(request):
    
    productos = Producto.objects.all()  # Obtener todos los productos
    usuarios = User.objects.all()  # Obtener todos los usuarios
    return render(request, 'admin/admin-index.html', {'productos': productos, 'usuarios': usuarios})


@api_view(['POST'])
def api_agregar_producto(request):
    # Asegúrate de pasar el 'request' en el contexto al inicializar el serializer
    serializer = ProductoSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        serializer.save()  # Guardar el producto
        return Response(serializer.data, status=status.HTTP_201_CREATED)  # Retornar el producto creado
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@require_http_methods(["PATCH"])
@login_required(login_url='/login/')
def producto_activo_desactivado(request, id):
    if not request.user.is_staff:
        return JsonResponse({'error': 'No tienes permisos para modificar productos.'}, status=403)
    
    try:
        producto = Producto.objects.get(id=id)
        producto.estado =  not producto.estado
        producto.save()
        return JsonResponse({'mensaje': 'Estado del producto actualizado correctamente', 'estado': producto.estado}, status=200)
    except Producto.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)

@api_view(['PUT'])
def api_editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    # Modifica el producto directamente sin almacenar el historial de precios
    serializer = ProductoSerializer(producto, data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    return render(request, 'admin/admin-editar-producto.html', {
        'producto': producto
    })

@api_view(['GET'])
def api_lista_productos(request):
    productos = Producto.objects.filter(estado=True)  # Solo los activos
    serializer = ProductoSerializer(productos, many=True)  # Serializa los productos
    return Response(serializer.data)





# ----------USUARIOS---------

class UserAdminView(APIView):
    def put(self, request, pk):
            # Cambiar los permisos de un usuario a 'staff'
        user = User.objects.get(pk=pk)
        user.is_staff = not user.is_staff  # Alternar entre staff y no staff
        user.save()
        return Response({"message": "Permisos de usuario actualizados"}, status=status.HTTP_200_OK)
    

@api_view(['PATCH'])
@login_required(login_url='/login/')
def cambiar_rol(request, id):
    if not request.user.is_staff:
        return JsonResponse({'error': 'No tienes permisos para modificar productos.'}, status=403)

    try:
        usuario = User.objects.get(id=id)
        usuario.is_staff =  not usuario.is_staff
        usuario.save()
        return JsonResponse({'mensaje': 'Estado del usuario actualizado correctamente', 'Rol': usuario.is_staff}, status=200)
    except Producto.DoesNotExist:
        return JsonResponse({'error': 'Rol no encontrado'}, status=404)
    



# ----------Ventas---------
@user_passes_test(lambda u: u.is_staff)
def VentasView(request):
    ventas = Venta_productos.objects.filter(estado_venta='pagado').select_related('id_usuario')
    return render(request, 'admin/admin-ventas.html', {'ventas': ventas})
