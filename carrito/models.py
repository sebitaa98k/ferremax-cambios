from django.db import models
from home.models import Producto 
from django.contrib.auth.models import User

class Venta_productos(models.Model):
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ventas')
    total_venta = models.IntegerField()
    fecha_transaccion = models.DateField(null=True, blank=True)
    estado_venta = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.fecha_transaccion} | {self.total_venta}"
    

class Carrito_detalle(models.Model):
    id_venta = models.ForeignKey(Venta_productos, on_delete=models.CASCADE, related_name='carrito_detalle')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='carrito_detalle')
    cantidad_producto = models.PositiveIntegerField()
    subtotal = models.IntegerField()

    def __str__(self):
        return f"{self.id_venta} | {self.producto.nombre} | {self.cantidad_producto} | {self.subtotal}"

    def save(self, *args, **kwargs):
        self.subtotal = self.producto.precio * self.cantidad_producto
        super().save(*args, **kwargs)

    @property
    def subtotal_venta(self):
        return self.producto.precio * self.cantidad_producto
