from rest_framework  import serializers
from .models import Producto

class ProductoSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='producto-detail', lookup_field='pk')
    imagen_url = serializers.URLField(required=False)
    
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'precio', 'descripcion', 'stock', 'imagen_url','estado', 'url']