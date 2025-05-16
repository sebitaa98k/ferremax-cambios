from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()  # Usamos el modelo de usuario que está configurado en AUTH_USER_MODEL
        fields = ['username', 'email', 'password', 'is_staff', 'is_superuser']  # Agregamos los campos is_staff y is_superuser
        
    def create(self, validated_data):
        # Crear el usuario
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        # Si el username es 'adminferremax123', lo hacemos superusuario
        if user.username == 'adminferremax123':
            user.is_superuser = True
            user.is_staff = True  # Si es el superusuario, también le damos permisos de staff

        # Si no es el admin, asignamos is_staff por defecto a False
        else:
            user.is_staff = False
            user.is_superuser = False  # Los usuarios normales no son superusuarios ni staff

        # Guardar el usuario con los permisos adecuados
        user.save()

        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
