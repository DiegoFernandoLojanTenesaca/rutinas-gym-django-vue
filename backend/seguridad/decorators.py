from functools import wraps
from django.http import JsonResponse
from http import HTTPStatus
from jose import jwt
from django.conf import settings
import time

def logueado():
    """
    Decorador para métodos de clase (APIView) que valida un JWT Bearer en Authorization.
    Uso: @logueado()
    """
    def _decorator(view_method):
        @wraps(view_method)
        def _wrapped(self, request, *args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return JsonResponse({'error': 'No autorizado'}, status=HTTPStatus.UNAUTHORIZED)

            parts = auth_header.split()
            if len(parts) != 2 or parts[0].lower() != 'bearer':
                return JsonResponse({'error': 'Formato de Authorization inválido'}, status=HTTPStatus.UNAUTHORIZED)

            token = parts[1]
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS512'])
            except Exception:
                return JsonResponse({'error': 'Token inválido'}, status=HTTPStatus.UNAUTHORIZED)

            # Validar expiración
            if int(payload.get("exp", 0)) <= int(time.time()):
                return JsonResponse({'error': 'Token expirado'}, status=HTTPStatus.UNAUTHORIZED)

            # Si todo OK, continuar
            return view_method(self, request, *args, **kwargs)
        return _wrapped
    return _decorator
