from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from .serializers import RegisterSerializer
from django.shortcuts import render
from django.contrib import messages

class RegisterView(APIView):
    def post(self, request):
        # Obtener los datos del formulario
        username = request.data.get('username')
        email = request.data.get('email')
        passw = request.data.get('password')
        passwr = request.data.get('passwordrepetir')

        # Comprobar si las contraseñas coinciden
        if passw != passwr:
            messages.error(request, 'Las contraseñas no son iguales.')
            return redirect('register')

        # Comprobar si el nombre de usuario ya está registrado
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso.')
            return redirect('register')
        
        # Comprobar si el correo electrónico ya está registrado
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Este correo electrónico ya está registrado.')
            return redirect('register')

        # Crear el usuario si todo es válido
        user = User.objects.create_user(username=username, email=email, password=passw)

        # Autenticamos al usuario automáticamente
        user = authenticate(request, username=username, password=passw)
        if user is not None:
            login(request, user)  # Se inicia la sesión del usuario
            return redirect('/')  # Redirige al home después de registro
        
        # Si no hay un error explícito, pero algo salió mal
        messages.error(request, 'Hubo un problema al autenticar al usuario')
        return redirect('register')

class LoginView(APIView):
    def post(self, request):
        # Obtener los datos del formulario de login
        username = request.data.get('username')
        password = request.data.get('password')

        # Intentar autenticar al usuario
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Iniciar sesión con el usuario autenticado
            login(request, user)

            if user.is_staff:
                # Redirigir a la página de admin o a una página personalizada para staff
                return redirect('/admin-index/')
            
            return redirect('/')  # Redirige al home si la autenticación fue exitosa
        
        # Si las credenciales no son válidas
        messages.error(request, 'Credenciales incorrectas o cuenta inactiva.')
        return redirect('login')    
    
    
def logout_view(request):
    # Eliminar la sesión del usuario
    logout(request)
    
    return JsonResponse({'message': 'Logout exitoso'}, status=200)

def Login_view(request):
    return render(request, 'account/login.html')


def Register_view(request):
    return render(request, 'account/register.html')



def get_username(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        return JsonResponse({'username':user.username})
    except User.DoesNotExist:
        return JsonResponse({'Error':'User not found'},status=404)