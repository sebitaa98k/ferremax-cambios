from django.urls import path
from .views import admin_view, api_agregar_producto, producto_activo_desactivado, api_editar_producto, editar_producto, api_lista_productos, cambiar_rol, VentasView
from .views import UserAdminView


urlpatterns = [
    path('admin-index/', admin_view, name='admin-index'),
    path('ver-ventas-generales/', VentasView, name='ver_ventas_generales' ),
    path('api/productos/agregar', api_agregar_producto, name='agregar_productos'),
    path('api/lista_producto/',api_lista_productos ,name='lista_producto_admin'),
    path('api/editar_producto/<int:id>/', api_editar_producto ,name='api_editar_producto'),
    path("editar_producto/<int:id>/", editar_producto, name="editar_producto"),
    path("api/cambiar_rol/<int:id>/", cambiar_rol, name="cambiar_rol"),
    path('api/user_admin/<int:pk>/', UserAdminView.as_view(), name='user_admin'),
    path('api/cambiar_activo/<int:id>/', producto_activo_desactivado, name='producto_activo_desactivado'),
]