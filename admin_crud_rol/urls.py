from django.urls import path
from . import views



urlpatterns = [
    path('admin-index/', views.admin_view, name='admin-index'),
]