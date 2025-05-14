from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from .serializers import RegisterSerializer, LoginSerializer
from django.shortcuts import render
from django.contrib import messages
from carrito.models import Venta_productos 
from rest_framework.authtoken.models import Token
from django.utils import timezone

class RegisterApiView(APIView):
    def post(self, request):
        # Obtener los datos del formulario
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        password_repeated = request.data.get('passwordrepetir')

        if password != password_repeated:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect('register')


        if User.objects.filter(email=email).exists():
            messages.error(request, "El correo electrónico ya está en uso.")
            return redirect('register')


        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está en uso.")
            return redirect('register')


        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            login(request, user)


            token, created = Token.objects.get_or_create(user=user)

            # Redirigir después de un registro exitoso
            return redirect('/')
        

        # Si el serializer no es válido, se redirige al registro con los errores
        for field, errors in serializer.errors.items():
            for error in errors:
                messages.error(request, error)

        return redirect('register') 
    

class LoginApiView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)

            token, created = Token.objects.get_or_create(user=user)

            response =  Response({
                'status': 'success',
                'message': 'Inicio de sesión exitoso',
                'token': token.key,
                'redirect_url': '/'
            },status=status.HTTP_200_OK)
        
            response.set_cookie('access_token', token.key, httponly=True, secure=False, max_age=3600, samesite='Lax')

            return response
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def Login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        
        user = authenticate(username=username, password= password)
        login(request, user)

        if not Venta_productos.objects.filter(id_usuario=user, estado_venta='carrito').exists():
                Venta_productos.objects.create(
                    id_usuario=user,
                    fecha_transaccion=timezone.now(),
                    total_venta=0.00,
                    estado_venta='carrito'
                )


        if user.is_staff:
                return redirect('admin-index')  # Redirige al panel de administración
        else:
                return redirect('/')
    
    return render(request, 'account/login.html')


    
def logout_view(request):
    # Eliminar la sesión del usuario
    logout(request)
    
    return JsonResponse({'message': 'Logout exitoso'}, status=200)



def Register_view(request):
    return render(request, 'account/register.html')



def get_username(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        return JsonResponse({'username':user.username})
    except User.DoesNotExist:
        return JsonResponse({'Error':'User not found'},status=404)