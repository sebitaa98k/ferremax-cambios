from django.urls import path
from . import views, api



urlpatterns = [
    path('', views.home_view, name='home'),
    path('catalogo/',views.listar_productos, name='catalogo'),
    path('productos/', api.ProductoListCreate.as_view(), name='producto'),
    path('productos/<int:pk>/', api.ProductoDetail.as_view(), name='producto-detail'),
]