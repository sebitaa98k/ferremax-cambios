from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import CarritoViewSet
from .views import view_carrito

# Crear un router y registrar el viewset del carrito
router = DefaultRouter()
router.register(r'carrito', CarritoViewSet)

# Incluir las rutas generadas por el router
urlpatterns = [
    path('api/', include(router.urls)),
    path('ver-carrito/', view_carrito, name='ver-carrito')
]
