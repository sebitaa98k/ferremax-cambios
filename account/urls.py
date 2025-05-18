from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import Register_view,Login_view, LoginApiView, RegisterApiView, get_username




urlpatterns = [
    path('api/register/', RegisterApiView.as_view(), name='register_api'),
    path('api/login/', LoginApiView.as_view(), name='login_api'),
    path('login/',Login_view, name='login'),
    path('register/', Register_view, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('api/get_username/<int:user_id>/', get_username, name='get_username'),

]