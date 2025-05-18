from django.contrib import admin
from .models import Venta_productos, Carrito_detalle

# Register your models here.
admin.site.register(Venta_productos)
admin.site.register(Carrito_detalle)