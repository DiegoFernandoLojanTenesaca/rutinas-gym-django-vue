from rest_framework.views import APIView
from django.http import JsonResponse
from http import HTTPStatus
from rest_framework.permissions import AllowAny
from .models import Contacto
from utilidades import utilidades
import threading

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class Clase1(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Crear un nuevo contacto",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del contacto'),
                'correo': openapi.Schema(type=openapi.TYPE_STRING, description='Correo del contacto'),
                'telefono': openapi.Schema(type=openapi.TYPE_STRING, description='Teléfono del contacto'),
                'mensaje': openapi.Schema(type=openapi.TYPE_STRING, description='Mensaje del contacto'),
            },
            required=['nombre', 'correo', 'telefono', 'mensaje']
        ),
        responses={
            201: openapi.Response(
                description="Contacto creado con éxito",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    example={"message": "Contacto guardado exitosamente"}
                )
            ),
            400: openapi.Response(
                description="Datos inválidos",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    example={"error": "El campo nombre es obligatorio"}
                )
            ),
            500: openapi.Response(
                description="Error interno",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    example={"error": "Error al guardar el contacto"}
                )
            ),
        }
    )
    def post(self, request):
        # Validaciones simples
        if not request.data.get("nombre"):
            return JsonResponse({"error": "El campo nombre es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        if not request.data.get("correo"):
            return JsonResponse({"error": "El campo correo es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        if not request.data.get("telefono"):
            return JsonResponse({"error": "El campo telefono es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        if not request.data.get("mensaje"):
            return JsonResponse({"error": "El campo mensaje es obligatorio"}, status=HTTPStatus.BAD_REQUEST)

        try:
            # Guardar en BD (fecha se setea sola con auto_now_add)
            Contacto.objects.create(
                nombre=request.data["nombre"],
                correo=request.data["correo"],
                telefono=request.data["telefono"],
                mensaje=request.data["mensaje"],
            )

            # Armar HTML del correo
            html = f"""
                <h1>Nuevo mensaje de contacto</h1>
                <ul>
                    <li><strong>Nombre:</strong> {request.data["nombre"]}</li>
                    <li><strong>Correo:</strong> {request.data["correo"]}</li>
                    <li><strong>Teléfono:</strong> {request.data["telefono"]}</li>
                    <li><strong>Mensaje:</strong> {request.data["mensaje"]}</li>
                </ul>
            """

            # Enviar email en un hilo (no bloquear la respuesta HTTP)
            threading.Thread(
                target=utilidades.enviar_contacto_mailtrap_sandbox,
                args=("Nuevo contacto", html, request.data["correo"]),
                daemon=True
            ).start()

            return JsonResponse({"message": "Contacto guardado exitosamente"}, status=HTTPStatus.CREATED)

        except Exception:
            return JsonResponse({"error": "Error al guardar el contacto"}, status=HTTPStatus.INTERNAL_SERVER_ERROR)
