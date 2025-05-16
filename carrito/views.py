from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Venta_productos, Carrito_detalle
from home.models import Producto
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from transbank.common.options import WebpayOptions
from transbank.common.integration_type import IntegrationType
from transbank.webpay.webpay_plus.transaction import Transaction
from .serializers import VentaSerializer, CarritoDetalleSerializer

def vista_carrito(request):
    if request.user.is_authenticated:
        # Obtener la venta activa con estado 'carrito'
        venta = Venta_productos.objects.filter(id_usuario=request.user, estado_venta='carrito').first()
        
        if venta:
            # Obtener los detalles del carrito
            carrito = Carrito_detalle.objects.filter(id_venta=venta)
            total_carrito = sum(item.subtotal for item in carrito)  # Calcular el total
            return render(request, 'carrito/carrito.html', {
                'carrito': carrito,
                'total_carrito': total_carrito,
            })
        else:
            return render(request, 'carrito/carrito.html', {'mensaje': 'No tienes productos en tu carrito.'})
    else:
        return render(request, 'carrito/carrito.html', {'mensaje': 'Por favor, inicia sesión para ver tu carrito.'})
    

@api_view(['GET','POST'])
def carrito_get_post(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            venta = Venta_productos.objects.filter(id_usuario=request.user, estado_venta='carrito').first()
            if venta:
                serializer = VentaSerializer(venta)
                return Response(serializer.data)
            return Response({"detail":"No hay carritos abierto."}, status=status.HTTP_404_NOT_FOUND)
        
        elif request.method == 'POST':
            venta = Venta_productos.objects.filter(
                id_usuario=request.user,
                fecha_compra=timezone.now(),
                total_venta=0,
                estado_venta='carrito'
            ) 

            detalles_data = request.data.get('detalles', [])
            for detalle_data in detalles_data:
                try:
                    producto = Producto.objects.get(id=detalle_data['producto'])
                    Carrito_detalle.objects.create(
                        id_venta=venta,
                        producto=producto,
                        cantidad_producto=detalle_data['cantidad_producto'],
                        subtotal=producto.precio * detalle_data['cantidad_producto']
                    )
                except Producto.DoesNotExist:
                    return Response({"detail": "Producto no encontrado."}, status=status.HTTP_400_BAD_REQUEST)
                
            return Response({"message": "Carrito creado exitosamente."}, status=status.HTTP_201_CREATED)
    return Response({"detail": "Usuario no autenticado."}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def agregar_carrito(request):
    if request.user.is_authenticated:
        try:
            venta = Venta_productos.objects.filter(id_usuario=request.user, estado_venta='carrito').first()
            if not venta:
                venta = Venta_productos.objects.create(
                    id_usuario=request.user,
                    fecha_transaccion=timezone.now(),
                    total_venta=0.00,
                    estado_venta='carrito'
                )
            
            producto_id = request.data.get('producto')
            cantidad = int(request.data.get('cantidad_producto') or 0)

            if cantidad <= 0:
                return Response({"detail": "La cantidad debe ser mayor que cero."}, status=status.HTTP_400_BAD_REQUEST)

            producto = Producto.objects.get(id=producto_id)

            detalle_existente = Carrito_detalle.objects.filter(id_venta=venta, producto=producto).first()

            if detalle_existente:
                nueva_cantidad = detalle_existente.cantidad_producto + cantidad

                if nueva_cantidad > producto.stock:
                    return Response({
                        "detail": f"No hay suficiente stock. Ya tienes {detalle_existente.cantidad_producto} y el stock total es {producto.stock}."
                    }, status=status.HTTP_400_BAD_REQUEST)

                detalle_existente.cantidad_producto = nueva_cantidad
                detalle_existente.subtotal = producto.precio * nueva_cantidad
                detalle_existente.save()
                mensaje = "Cantidad actualizada en el carrito."
            else:
                if cantidad > producto.stock:
                    return Response({
                        "detail": f"No hay suficiente stock. Solo quedan {producto.stock} unidades disponibles."
                    }, status=status.HTTP_400_BAD_REQUEST)

                Carrito_detalle.objects.create(
                    id_venta=venta,
                    producto=producto,
                    cantidad_producto=cantidad,
                    subtotal=producto.precio * cantidad
                )
                mensaje = "Producto agregado al carrito exitosamente."

            venta.total_venta = sum(d.subtotal for d in venta.carrito_detalle.all())
            venta.save()

            return Response({"message": mensaje})

        except Producto.DoesNotExist:
            return Response({"detail": "Producto no encontrado."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": f"Error al agregar producto al carrito: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({"detail": "Usuario no autenticado."}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def eliminar_o_disminuir_producto(request, detalle_id):
    if request.user.is_authenticated:
        try:
            detalle = Carrito_detalle.objects.get(id=detalle_id)
        except Carrito_detalle.DoesNotExist:
            return Response({"detail": "Producto no encontrado en el carrito."}, status=status.HTTP_404_NOT_FOUND)

        # Si la cantidad es 1, eliminamos el producto del carrito
        if detalle.cantidad_producto == 1:
            detalle.delete()
            venta = detalle.id_venta
            venta.total_venta = sum(d.subtotal for d in venta.carrito_detalle.all())  # Aseguramos que la relación esté correcta
            venta.save()
            return Response({"message": "Producto eliminado del carrito", "total_carrito": venta.total_venta})

        # Si la cantidad es mayor a 1, decrementamos la cantidad
        detalle.cantidad_producto -= 1
        detalle.subtotal = detalle.producto.precio * detalle.cantidad_producto
        detalle.save()

        # Actualizamos el total de la venta
        venta = detalle.id_venta
        venta.total_venta = sum(d.subtotal for d in venta.carrito_detalle.all())
        venta.save()

        return Response({
            "subtotal_venta": detalle.subtotal,
            "total_carrito": venta.total_venta
        })
    return Response({"detail": "Usuario no autenticado."}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def actualizar_cantidad_producto(request, detalle_id):
    if request.user.is_authenticated:
        try:
            detalle = Carrito_detalle.objects.get(id=detalle_id)
        except Carrito_detalle.DoesNotExist:
            return Response({"detail": "Producto no encontrado en el carrito."}, status=status.HTTP_404_NOT_FOUND)

        # Obtener la nueva cantidad del cuerpo de la solicitud
        nueva_cantidad = request.data.get('cantidad_producto')

        if nueva_cantidad <= 0:
            # Si la cantidad es menor a 1, eliminamos el producto
            detalle.delete()
            venta = detalle.id_venta
            venta.total_venta = sum(d.subtotal for d in venta.carrito_detalle.all())
            venta.save()
            return Response({"message": "Producto eliminado del carrito.", "total_carrito": venta.total_venta})

        # Verificar si la cantidad es mayor al stock disponible
        if nueva_cantidad > detalle.producto.stock:
            return Response({"detail": f"No hay suficiente stock. Solo quedan {detalle.producto.stock} unidades disponibles."},
            status=status.HTTP_400_BAD_REQUEST)

        # Actualizamos la cantidad y el subtotal
        detalle.cantidad_producto = nueva_cantidad
        detalle.subtotal = detalle.producto.precio * nueva_cantidad  # Aquí calculamos el nuevo subtotal
        detalle.save()

        # Actualizamos el total de la venta
        venta = detalle.id_venta
        venta.total_venta = sum(d.subtotal for d in venta.carrito_detalle.all())
        venta.save()

        return Response({
            "subtotal_total": detalle.subtotal,  # Subtotal calculado correctamente
            "total_carrito": venta.total_venta
        })
    return Response({"detail": "Usuario no autenticado."}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def pagar_webpy(request):
    print('Redirijiendo')
    if not request.user.is_authenticated:
        return Response({'Error':'Debes iniciar sesion'},status=401)
    
    venta = Venta_productos.objects.filter(id_usuario=request.user, estado_venta='carrito').first()
    if not venta:
        return Response({'Error':'No tienes carrito antiguo'}, status=404)
    
    venta.save()

    options = WebpayOptions(
        commerce_code='597055555532',
        api_key='579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C',
        integration_type=IntegrationType.TEST
    )

    tx = Transaction(options)
    import time
    buy_order = f"{venta.id}-{int(time.time())}"
    return_url = request.build_absolute_uri('/api/webpay/respuesta/')

    response = tx.create(
        buy_order=buy_order,
        session_id=str(request.user.id),
        amount=venta.total_venta,
        return_url=return_url
    )

    # Imprime la respuesta completa de Webpay
    print("Response de Webpay:", response)

    # Verifica que la respuesta contenga la URL correcta
    if 'url' in response:
        print("Webpay URL:", response['url'])
        return redirect(response['url'] + "?token_ws=" + response['token'])
    else:
        print("Error: No se recibió la URL de Webpay")
        return Response({"error": "No se pudo obtener la URL de Webpay"}, status=500)

    venta.webpay_transaction_id = response['token']
    venta.save()

    return redirect(response['url']+ "?tokwn_ws=" + response['token'])




@csrf_exempt
@require_http_methods(["GET", "POST"])
def respuesta_pago_webpay(request):
    token = request.POST.get("token_ws") or request.GET.get("token_ws")


    if not token:
        return redirect('/carrito/?mensaje=Transacción cancelada.')



    options = WebpayOptions(
        commerce_code='597055555532',
        api_key='579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C',
        integration_type=IntegrationType.TEST
    )

    # Verificar el estado del pago con el token recibido
    tx = Transaction(options)

    try:
        response = tx.commit(token)
        id_venta = str(response['buy_order']).split("-")[0]
        venta = Venta_productos.objects.get(id=int(id_venta))

        if not venta.carrito_detalle.exists():
            return HttpResponse("No puedes completar el pago: el carrito está vacío.")

        if response['status'] == 'AUTHORIZED':
            venta.estado_venta = 'pagado'
            venta.fecha_compra = timezone.now()
            venta.webpay_payment_status = 'completed'

            # ✅ Calcular total antes de guardar
            venta.total_venta = sum(d.subtotal_venta for d in venta.carrito_detalle.all())
            venta.save()

            for detalle in venta.carrito_detalle.all():
                producto = detalle.producto
                producto.stock -= detalle.cantidad_producto


                if producto.stock <= 0:
                    producto.stock = 0  # por si acaso quedó negativo
                    producto.estado = False

                producto.save()


            mensaje = "✅ Pago realizado con éxito"

        else:
            venta.webpay_payment_status = 'failed'
            venta.save()
            mensaje = "❌ Pago rechazado"
    except Exception as e:
        return HttpResponse(f"<b>Error al procesar la transacción:</b> {e}")

    return render(request, 'carrito/respuesta_compra.html', {
        'mensaje': mensaje,
        'venta': venta,
        'response': response
    })


