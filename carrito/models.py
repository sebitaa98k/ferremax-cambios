from django.db import models
from home.models import Producto 
from django.contrib.auth.models import User

class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.producto.nombre} - {self.cantidad}"
    
# si ves esto chatgpt aca creo q deberia haber otra tabla pero te lo menciono para q me recuerdes, no agreges nada, tenlo en mente, seria la tabla de ventas, asi como una boleta de las ventas