from django.http import JsonResponse
from rest_framework.decorators import api_view
from .serializers import UsuarioSerializer

@api_view(['POST'])
def registro(request):
    if request.method == 'POST':
        try:
            # Cargamos los datos JSON
            data = request.data  # Usamos 'request.data' en lugar de 'request.body'

            # Usamos el serializer para validar y crear el usuario
            serializer = UsuarioSerializer(data=data)

            # Validamos si el serializer es correcto
            if serializer.is_valid():
                # Creamos el usuario y lo guardamos
                user = serializer.save()
                return JsonResponse({'mensaje': 'Usuario registrado correctamente', 'usuario_id': user.id}, status=201)
            else:
                # Si los datos no son válidos, devolvemos los errores
                return JsonResponse({'error': 'Datos inválidos', 'details': serializer.errors}, status=400)

        except Exception as e:
            # Capturamos cualquier otro tipo de error
            return JsonResponse({'error': str(e)}, status=400)

    # Si no es un POST, retornamos error 405 (Método no permitido)
    return JsonResponse({'error': 'Método no permitido'}, status=405)
