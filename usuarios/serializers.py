from rest_framework import serializers
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    # Campos para validar las contraseñas
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ['nombre', 'correo_electronico', 'password1', 'password2', 'estado']

    def validate(self, data):
        """
        Verifica si las contraseñas coinciden.
        """
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({"password1": "Las contraseñas no coinciden."})
        return data

    def create(self, validated_data):
        """
        Crea el usuario y guarda la contraseña de manera segura.
        """
        validated_data.pop('password2')  # No necesitamos guardar el segundo campo
        
        # Asignamos el estado por defecto si no está presente
        if 'estado' not in validated_data:
            validated_data['estado'] = 'activo'  # Valor por defecto

        # Creamos el usuario con los datos validados
        user = Usuario(
            nombre=validated_data['nombre'],
            correo_electronico=validated_data['correo_electronico'],
            estado=validated_data['estado']  # Usamos el valor del estado
        )
        
        # Hasheamos la contraseña y la guardamos
        user.set_password(validated_data['password1'])
        user.save()
        return user
