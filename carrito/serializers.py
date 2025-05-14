from rest_framework import serializers
from .models import Carrito_detalle, Venta_productos
from home.models import Producto

class CarritoDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrito_detalle
        fields = ['producto', 'cantidad_producto', 'subtotal', 'id_venta']    

        def validate_cantidad_producto(self, value):
            if value <= 0:
                raise serializers.ValidationError('La cantidad del producto debe ser mayor que 0')
            return value
        
class VentaSerializer(serializers.ModelSerializer):
    carrito_detalle = CarritoDetalleSerializer(many=True)

    class Meta:
        model = Venta_productos
        fields = ['id', 'fecha_transaccion', 'total_venta', 'estado_venta', 'id_usuario', 'carrito_detalle']

    def create(self, validated_data):
        carrito_detalle_data = validated_data.pop('carrito_detalle')  # Aquí también cambiamos 'detalle' por 'carrito_detalle'
        venta = Venta_productos.objects.create(**validated_data)
        for detalle_data in carrito_detalle_data:
            Carrito_detalle.objects.create(id_venta=venta, **detalle_data)
        return venta