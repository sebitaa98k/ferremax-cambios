from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('catalogo/',views.listar_productos, name='catalogo'),
    path('api/tasa/', views.obtener_tasa, name='tasa_cambio'),
    path('test/404/', views.test_404_view, name='404'),
]

