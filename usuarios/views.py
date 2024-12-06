from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
import json
from .serializers import UsuarioSerializer

User = get_user_model()

@csrf_exempt
def registro(request):
    if request.method == 'POST':
        try:
            # Cargamos los datos JSON
            data = json.loads(request.body)

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

        except json.JSONDecodeError:
            # Si no es un JSON válido, devolvemos el error correspondiente
            return JsonResponse({'error': 'JSON inválido'}, status=400)

    # Si no es un POST, retornamos error 405 (Método no permitido)
    return JsonResponse({'error': 'Método no permitido'}, status=405)
