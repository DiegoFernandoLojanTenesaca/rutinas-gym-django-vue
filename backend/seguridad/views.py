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
            UsersMetadata.objects.filter(pk=meta.pk).update(token="")

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
