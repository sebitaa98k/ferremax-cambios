from rest_framework  import serializers
from .models import Producto

class ProductoSerializer(serializers.ModelSerializer):
    imagen_url = serializers.URLField(required=False)
    
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'precio', 'descripcion', 'stock', 'imagen_url','estado']