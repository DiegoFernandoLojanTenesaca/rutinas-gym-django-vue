from rest_framework.views import APIView
from django.http import JsonResponse, HttpResponseRedirect
from http import HTTPStatus
from rest_framework.permissions import AllowAny
from .models import UsersMetadata
from django.contrib.auth.models import User
from uuid import uuid4
import os
from utilidades import utilidades
from django.contrib.auth import authenticate
from jose import jwt
from django.conf import settings
from datetime import datetime, timedelta
import time
from django.utils import timezone

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from seguridad.decorators import logueado

class Clase1(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Registrar un nuevo usuario",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del usuario'),
                'correo': openapi.Schema(type=openapi.TYPE_STRING, description='Correo del usuario'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Contraseña del usuario'),
            },
            required=['nombre', 'correo', 'password']
        ),
        responses={
            201: openapi.Response(
                description="Usuario creado con éxito",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    example={"message": "Usuario registrado correctamente"}
                )
            ),
            400: openapi.Response(
                description="Error en los datos enviados",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    example={"error": "El correo ya está en uso"}
                )
            ),
            500: openapi.Response(
                description="Error interno del servidor",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    example={"error": "Error interno del servidor"}
                )
            )
        }
    )
    def post(self, request):
        if not request.data.get("nombre"):
            return JsonResponse({'error': 'El campo nombre es obligatorio'}, status=HTTPStatus.BAD_REQUEST)
        if not request.data.get("correo"):
            return JsonResponse({'error': 'El campo correo es obligatorio'}, status=HTTPStatus.BAD_REQUEST)
        if not request.data.get("password"):
            return JsonResponse({'error': 'El campo password es obligatorio'}, status=HTTPStatus.BAD_REQUEST)

        if User.objects.filter(email=request.data.get("correo")).exists():
            return JsonResponse({'error': 'El correo ya está en uso'}, status=HTTPStatus.BAD_REQUEST)

        token = str(uuid4())
        base_url = os.getenv('BASE_URL', 'http://127.0.0.1:8000/')
        if not base_url.endswith('/'):
            base_url += '/'
        url = f"{base_url}api/v1/seguridad/verificacion/{token}"

        try:
            u = User.objects.create_user(
                username=request.data["correo"],
                password=request.data["password"],
                email=request.data["correo"],
                first_name=request.data["nombre"],
                last_name="",
                is_active=0
            )
            UsersMetadata.objects.create(token=token, user_id=u.id)

            html = f"""
            <h1>Bienvenido a nuestra plataforma</h1>
            <p>Hola {request.data['nombre']}, gracias por registrarte.</p>
            <p>Por favor verifica tu correo haciendo clic en el siguiente enlace:</p>
            <a href="{url}">Verificar correo</a>
            <p>Si no te registraste, ignora este mensaje.</p>
            """

            utilidades.enviar_contacto_mailtrap_sandbox(
                asunto="Verificación de correo",
                html=html,
                destinatario=request.data["correo"]
            )

        except Exception:
            return JsonResponse({'error': 'Error interno del servidor'}, status=HTTPStatus.BAD_REQUEST)

        return JsonResponse({'message': 'Usuario registrado correctamente'}, status=HTTPStatus.CREATED)


class Clase2(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Verificar el correo del usuario",
        manual_parameters=[
            openapi.Parameter(
                'token',
                openapi.IN_PATH,
                description="Token de verificación",
                type=openapi.TYPE_STRING
            )
        ],
        responses={
            200: openapi.Response(
                description="Correo verificado con éxito",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    example={"message": "Correo verificado correctamente"}
                )
            ),
            400: openapi.Response(
                description="Token inválido o ya utilizado",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    example={"error": "Token inválido o ya utilizado"}
                )
            ),
            500: openapi.Response(
                description="Error interno del servidor",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    example={"error": "Error interno del servidor"}
                )
            )
        }
    )
    def get(self, request, token):
        if not token:
            return JsonResponse({'error': 'Recurso no disponible'}, status=HTTPStatus.NOT_FOUND)

        try:
            meta = UsersMetadata.objects.get(token=token, user__is_active=0)
            User.objects.filter(id=meta.user_id).update(is_active=1)
            # Consumir el token
            #UsersMetadata.objects.filter(pk=meta.pk).update(token="")
            UsersMetadata.objects.filter(pk=meta.pk).update(token=None)

            frontend_url = os.getenv('BASE_URL_FRONTEND', '')
            return HttpResponseRedirect(frontend_url if frontend_url else '/')

        except UsersMetadata.DoesNotExist:
            return JsonResponse({'error': 'Token inválido o ya utilizado'}, status=HTTPStatus.BAD_REQUEST)
        except Exception:
            return JsonResponse({'error': 'Error interno del servidor'}, status=HTTPStatus.INTERNAL_SERVER_ERROR)


class Clase3(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Iniciar sesión de usuario",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'correo': openapi.Schema(type=openapi.TYPE_STRING, description='Correo del usuario'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Contraseña del usuario'),
            },
            required=['correo', 'password']
        ),
        responses={
            200: openapi.Response(
                description="Inicio de sesión exitoso",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    example={
                        "id": 1,
                        "nombre": "Diego",
                        "token": "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9..."
                    }
                )
            ),
            400: openapi.Response(
                description="Error en los datos enviados",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    example={"error": "El campo correo es obligatorio"}
                )
            ),
            404: openapi.Response(
                description="Usuario no encontrado",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    example={"error": "Recurso no disponible"}
                )
            ),
            401: openapi.Response(
                description="Credenciales inválidas",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    example={"error": "Credenciales inválidas"}
                )
            ),
            500: openapi.Response(
                description="Error interno del servidor",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    example={"error": "Error interno del servidor"}
                )
            )
        }
    )
    def post(self, request):
        if not request.data.get("correo"):
            return JsonResponse({'error': 'El campo correo es obligatorio'}, status=HTTPStatus.BAD_REQUEST)
        if not request.data.get("password"):
            return JsonResponse({'error': 'El campo password es obligatorio'}, status=HTTPStatus.BAD_REQUEST)

        try:
            user = User.objects.filter(email=request.data["correo"]).get()
        except User.DoesNotExist:
            return JsonResponse({'error': 'Recurso no disponible'}, status=HTTPStatus.NOT_FOUND)

        auth = authenticate(request, username=request.data.get("correo"), password=request.data.get("password"))
        if auth is not None:
            ahora = timezone.now()
            exp = ahora + timedelta(days=1)
            payload = {
                "id": user.id,
                "ISS": os.getenv('BASE_URL') or '',
                "iat": int(time.time()),
                "exp": int(exp.timestamp()),
            }

            try:
                token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS512')
                return JsonResponse({"id": user.id, "nombre": user.first_name, "token": token})
            except Exception:
                return JsonResponse({'error': 'Error interno del servidor'}, status=HTTPStatus.INTERNAL_SERVER_ERROR)

        return JsonResponse({'error': 'Credenciales inválidas'}, status=HTTPStatus.UNAUTHORIZED)
    

    # Helper: obtener user_id desde Authorization (mismo esquema que ya usas)
def _get_user_id_from_request(request):
    try:
        header = (request.headers.get('Authorization') or "").split(" ")
        token = header[1] if len(header) == 2 else ""
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS512'])
        return int(payload.get("id"))
    except Exception:
        return None


class PerfilMeView(APIView):
    """
    GET  /api/v1/usuarios/me        -> devuelve {id, nombre, correo}
    PUT  /api/v1/usuarios/me        -> actualiza nombre/correo
    """
    permission_classes = [AllowAny]

    @logueado()
    def get(self, request):
        user_id = _get_user_id_from_request(request)
        if not user_id:
            return JsonResponse({'error': 'No autorizado'}, status=HTTPStatus.UNAUTHORIZED)

        try:
            u = User.objects.get(pk=user_id)
            data = {'id': u.id, 'nombre': u.first_name, 'correo': u.email}
            return JsonResponse({'data': data}, status=HTTPStatus.OK)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=HTTPStatus.NOT_FOUND)

    @logueado()
    def put(self, request):
        user_id = _get_user_id_from_request(request)
        if not user_id:
            return JsonResponse({'error': 'No autorizado'}, status=HTTPStatus.UNAUTHORIZED)

        nombre = (request.data.get('nombre') or '').strip()
        correo = (request.data.get('correo') or '').strip()

        if not nombre:
            return JsonResponse({'error': 'El campo nombre es obligatorio'}, status=HTTPStatus.BAD_REQUEST)
        if not correo:
            return JsonResponse({'error': 'El campo correo es obligatorio'}, status=HTTPStatus.BAD_REQUEST)

        try:
            u = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=HTTPStatus.NOT_FOUND)

        # si cambió el correo, valida que no esté en uso
        if correo.lower() != (u.email or '').lower():
            if User.objects.filter(email=correo).exclude(pk=u.id).exists():
                return JsonResponse({'error': 'El correo ya está en uso'}, status=HTTPStatus.BAD_REQUEST)

        # actualizar (mantenemos username = correo para coherencia)
        u.first_name = nombre
        u.email = correo
        u.username = correo
        try:
            u.save()
            return JsonResponse({'message': 'Perfil actualizado'}, status=HTTPStatus.OK)
        except Exception:
            return JsonResponse({'error': 'No se pudo actualizar el perfil'}, status=HTTPStatus.BAD_REQUEST)


class CambiarPasswordView(APIView):
    """
    PUT /api/v1/usuarios/me/password
    body: { "actual": "...", "nueva": "..." }
    """
    permission_classes = [AllowAny]

    @logueado()
    def put(self, request):
        user_id = _get_user_id_from_request(request)
        if not user_id:
            return JsonResponse({'error': 'No autorizado'}, status=HTTPStatus.UNAUTHORIZED)

        actual = request.data.get('actual') or ''
        nueva = request.data.get('nueva') or ''
        if not actual or not nueva:
            return JsonResponse({'error': 'Campos actual y nueva son obligatorios'}, status=HTTPStatus.BAD_REQUEST)
        if len(nueva) < 6:
            return JsonResponse({'error': 'La nueva contraseña debe tener al menos 6 caracteres'}, status=HTTPStatus.BAD_REQUEST)

        try:
            u = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=HTTPStatus.NOT_FOUND)

        if not u.check_password(actual):
            return JsonResponse({'error': 'Contraseña actual incorrecta'}, status=HTTPStatus.UNAUTHORIZED)

        try:
            u.set_password(nueva)
            u.save()
            return JsonResponse({'message': 'Contraseña actualizada'}, status=HTTPStatus.OK)
        except Exception:
            return JsonResponse({'error': 'No se pudo actualizar la contraseña'}, status=HTTPStatus.BAD_REQUEST)


