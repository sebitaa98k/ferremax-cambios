from django.urls import path
from .views import admin_view, api_agregar_producto, producto_activo_desactivado
from .views import UserAdminView


urlpatterns = [
    path('admin-index/', admin_view, name='admin-index'),
    path('api/productos/agregar', api_agregar_producto, name='agregar_productos'),
    path('api/user_admin/<int:pk>/', UserAdminView.as_view(), name='user_admin'),
    path('api/cambiar_activo/<int:id>/', producto_activo_desactivado, name='producto_activo_desactivado'),
]