from rest_framework import serializers
from .models import Carrito
from home.models import Producto

class CarritoSerializer(serializers.ModelSerializer):
    producto = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all())

    class Meta:
        model = Carrito
        fields = ['id', 'usuario', 'producto', 'cantidad', 'fecha_agregado']