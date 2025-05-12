from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib import messages
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer
from django.shortcuts import render, redirect  
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny

# Vista para el api rest del registro
class RegisterView(APIView):
    def post(self, request):
        permission_classes = [AllowAny]
        # Obtener los datos del formulario
        username = request.data.get('username')
        email = request.data.get('email')
        passw = request.data.get('password')
        passwr = request.data.get('passwordrepetir')

        # Comprobar si el nombre de usuario ya está registrado
        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está en uso.")
        
        # Comprobar si el correo electrónico ya está registrado
        if User.objects.filter(email=email).exists():
            messages.error(request, "Este correo electrónico ya está registrado.")

        ## aca necesito otro mensaje pero esta vez diciendo que las contraseñas no son iguales
        
        if passw != passwr:
            messages.error(request,'Las contraseñas no son iguales')

        # Si hay mensajes de error, no continuar con el registro
        if messages.get_messages(request):
            return redirect('register')  # Redirige si hay errores

        # Si no hay errores, proceder a crear el usuario
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Redirigir al login después de crear el usuario
            response = JsonResponse({"message": "Usuario creado correctamente"})
            response['Location'] = '/login/'  # Redirigir a login
            response.status_code = 302
            return response
        
        # Si el serializer no es válido, devolver los errores como mensajes en el frontend
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vista para el api rest del login
class LoginView(APIView):
    permission_classes = [AllowAny]
    @csrf_exempt
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                request, username=serializer.validated_data['username'], password=serializer.validated_data['password']
            )
            if user is not None:
                # Crear los tokens JWT
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                refresh.payload['username'] = user.username
                refresh.payload['role'] = 'staff' if user.is_staff else 'regular'  # Agregar el rol al JWT

                # Establecer el token en una cookie
                response = JsonResponse({'message': 'Login successful'})
                response.set_cookie('access_token', access_token, httponly=False, secure=True, max_age=3600, samesite='Lax')

                # Si el usuario es staff, mostramos el mensaje en la consola del navegador
                if user.is_staff:
                    response['Location'] = '/admin_crud_rol/admin-index/'
                    response.status_code = 302

                else:
                    # Redirigir al home si no es staff
                    response['Location'] = '/'
                    response.status_code = 302

                return response

            # Si las credenciales son incorrectas
            messages.error(request, 'Cuenta no encontrada o credenciales incorrectas.')
            return redirect('login')

        # Si el serializer no es válido
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vista para el frontend (ejemplo de una página de login con un formulario tradicional)
def Login_view(request):
    return render(request, 'account/login.html')


def Register_view(request):
    return render(request, 'account/register.html')


def logout_view(request):
    # Eliminar la cookie del access_token
    response = JsonResponse({'message': 'Logout successful'})
    response.delete_cookie('access_token')  # Esto elimina la cookie 'access_token'
    
    return response

def get_username(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        return JsonResponse({'username':user.username})
    except User.DoesNotExist:
        return JsonResponse({'Error':'User not found'},status=404)