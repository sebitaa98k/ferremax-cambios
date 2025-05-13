from django.urls import path
from .views import admin_view, ProductoView
from .views import UserAdminView


urlpatterns = [
    path('admin-index/', admin_view, name='admin-index'),
    path('api/productos/', ProductoView.as_view(), name='productos'),
    path('api/productos/<int:pk>/', ProductoView.as_view(), name='producto_detail'),
    path('api/user_admin/<int:pk>/', UserAdminView.as_view(), name='user_admin'),
]