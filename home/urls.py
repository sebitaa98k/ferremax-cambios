from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_view, name='home'),
    path('catalogo/',views.listar_productos, name='catalogo'),
    path('historia_compras/',views.HistorialComprasView, name='historial_compras'),
    path('boleta_compras/<int:id>/', views.BoletaVenta, name='boleta_compra'),
]