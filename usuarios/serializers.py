from rest_framework import serializers
from django.contrib.auth import get_user_model

# Usamos el modelo de usuario que has configurado
User = get_user_model()

class UsuarioSerializer(serializers.ModelSerializer):
    # Campos que deseas recibir
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['nombre', 'correo_electronico', 'password1', 'password2']

    def validate(self, data):
        """
        Verifica si las contraseñas coinciden
        """
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({"password1": "Las contraseñas no coinciden."})
        return data

    def create(self, validated_data):
        """
        Crea el usuario y guarda la contraseña de manera segura.
        """
        # Eliminamos las contraseñas para que no se guarden en validated_data
        validated_data.pop('password2')

        # Creamos el usuario
        user = User.objects.create_user(
            nombre=validated_data['nombre'],
            correo_electronico=validated_data['correo_electronico'],
            password=validated_data['password1']
        )
        return user
