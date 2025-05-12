from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('home.urls')),
    path('', include('account.urls')),
    path('admin_crud_rol/',include('admin_crud_rol.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('carrito/', include('carrito.urls')),
]
