from rest_framework.views import APIView
from django.http.response import JsonResponse
from http import HTTPStatus
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from seguridad.decorators import logueado
from django.utils.dateformat import DateFormat
from ejercicios.serializers import EjercicioSerializer
from ejercicios.models import Ejercicio
import os
from django.core.files.storage import FileSystemStorage
from datetime import datetime
from categorias.models import Categoria
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class Clase1(APIView):
    permission_classes = [AllowAny]

    @logueado()
    @swagger_auto_schema(
        operation_description="Actualizar SOLO la foto de un ejercicio existente",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del ejercicio'),
                'foto': openapi.Schema(type=openapi.TYPE_FILE, description='Foto del ejercicio'),
            },
            required=['id', 'foto']
        ),
        responses={
            200: openapi.Response(
                description="Foto actualizada correctamente",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    example={"msg": "Ejercicio actualizado correctamente"}
                )
            ),
            400: openapi.Response(
                description="Error en los datos o archivo inválido",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    example={"error": "El campo id es obligatorio"}
                )
            ),
            404: openapi.Response(
                description="Ejercicio no encontrado",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    example={"error": "Ejercicio no encontrado"}
                )
            ),
        }
    )
    def post(self, request):
        if not request.data.get("id"):
            return JsonResponse({"error": "El campo id es obligatorio"}, status=HTTPStatus.BAD_REQUEST)

        try:
            existe = Ejercicio.objects.filter(id=request.data["id"]).get()
            anterior = existe.foto
        except Ejercicio.DoesNotExist:
            return JsonResponse({"error": "Ejercicio no encontrado"}, status=HTTPStatus.BAD_REQUEST)

        fs = FileSystemStorage()
        try:
            foto = f"{datetime.timestamp(datetime.now())}{os.path.splitext(str(request.FILES['foto']))[1]}"
        except Exception:
            return JsonResponse({"error": "Error: se debe adjuntar una imagen"}, status=HTTPStatus.BAD_REQUEST)

        if request.FILES["foto"].content_type in ["image/jpeg", "image/png"]:
            try:
                # Guardará en MEDIA_ROOT/ejercicios/<archivo>
                fs.save(f"ejercicios/{foto}", request.FILES['foto'])
                Ejercicio.objects.filter(id=request.data["id"]).update(foto=foto)

                # Borrar archivo anterior si existía
                ruta_anterior = f"./upload/ejercicios/{anterior}"
                if anterior and os.path.exists(ruta_anterior):
                    os.remove(ruta_anterior)

                return JsonResponse({"msg": "Ejercicio actualizado correctamente"}, status=HTTPStatus.OK)
            except Exception:
                return JsonResponse({"error": "Se produjo un error al intentar actualizar el ejercicio"}, status=HTTPStatus.BAD_REQUEST)
        else:
            return JsonResponse({"error": "El archivo debe ser una imagen JPEG o PNG"}, status=HTTPStatus.BAD_REQUEST)


class Clase2(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Obtener un ejercicio específico por su slug",
        manual_parameters=[
            openapi.Parameter(
                'slug',
                openapi.IN_PATH,
                description="Slug del ejercicio",
                type=openapi.TYPE_STRING
            )
        ],
        responses={
            200: openapi.Response(
                description="Datos del ejercicio",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    example={
                        "data": {
                            "id": 1,
                            "nombre": "Press de banca",
                            "slug": "press-de-banca",
                            "tiempo": "3x10",
                            "descripcion": "Ejercicio de pecho con barra",
                            "fecha": "01/09/2025",
                            "categoria": "Pecho",
                            "categoria_id": 2,
                            "imagen": "http://127.0.0.1:8000/upload/ejercicios/press.png",
                            "user_id": 1,
                            "user": "Diego"
                        }
                    }
                )
            ),
            404: openapi.Response(
                description="Ejercicio no encontrado",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    example={"error": "Ejercicio no encontrado"}
                )
            )
        }
    )
    def get(self, request, slug):
        try:
            data = Ejercicio.objects.filter(slug=slug).get()
            return JsonResponse({"data": {
                "id": data.id,
                "nombre": data.nombre,
                "slug": data.slug,
                "tiempo": data.tiempo,
                "descripcion": data.descripcion,
                "fecha": DateFormat(data.fecha).format('d/m/Y'),
                "categoria": data.categoria.nombre,
                "categoria_id": data.categoria_id,
                "imagen": f"{os.getenv('BASE_URL')}upload/ejercicios/{data.foto}",
                "user_id": data.user_id,
                "user": data.user.first_name
            }}, status=HTTPStatus.OK)
        except Ejercicio.DoesNotExist:
            return JsonResponse({"error": "Ejercicio no encontrado"}, status=HTTPStatus.NOT_FOUND)


class Clase3(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Obtener 3 ejercicios aleatorios",
        responses={
            200: openapi.Response(
                description="Lista de ejercicios aleatorios",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    example={
                        "data": [
                            {"id": 1, "nombre": "Dominadas", "slug": "dominadas"},
                            {"id": 2, "nombre": "Sentadillas", "slug": "sentadillas"},
                            {"id": 3, "nombre": "Press militar", "slug": "press-militar"}
                        ]
                    }
                )
            )
        }
    )
    def get(self, request):
        data = Ejercicio.objects.order_by('?').all()[:3]
        datos_json = EjercicioSerializer(data, many=True)
        return JsonResponse({"data": datos_json.data}, status=HTTPStatus.OK)


class Clase4(APIView):
    permission_classes = [AllowAny]

    @logueado()
    @swagger_auto_schema(
        operation_description="Obtener ejercicios creados por un usuario específico",
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="ID del usuario",
                type=openapi.TYPE_INTEGER
            )
        ],
        responses={
            200: openapi.Response(
                description="Lista de ejercicios del usuario",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    example={
                        "data": [
                            {"id": 1, "nombre": "Remo con barra", "slug": "remo-con-barra"},
                            {"id": 2, "nombre": "Fondos en paralelas", "slug": "fondos-en-paralelas"}
                        ]
                    }
                )
            ),
            404: openapi.Response(
                description="Usuario no encontrado",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    example={"error": "Usuario no encontrado"}
                )
            )
        }
    )
    def get(self, request, id):
        try:
            User.objects.filter(id=id).get()
        except User.DoesNotExist:
            return JsonResponse({"error": "Usuario no encontrado"}, status=HTTPStatus.BAD_REQUEST)

        data = Ejercicio.objects.filter(user_id=id).order_by('-id').all()
        datos_json = EjercicioSerializer(data, many=True)
        return JsonResponse({"data": datos_json.data}, status=HTTPStatus.OK)


class Clase5(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Buscar ejercicios por categoría y texto",
        manual_parameters=[
            openapi.Parameter(
                'categoria_id',
                openapi.IN_QUERY,
                description="ID de la categoría",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Texto a buscar en el nombre del ejercicio",
                type=openapi.TYPE_STRING,
                required=False
            )
        ],
        responses={
            200: openapi.Response(
                description="Lista de ejercicios encontrados",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    example={
                        "data": [
                            {"id": 1, "nombre": "Curl bíceps con barra", "slug": "curl-biceps-barra"},
                            {"id": 2, "nombre": "Press inclinado", "slug": "press-inclinado"}
                        ]
                    }
                )
            ),
            400: openapi.Response(
                description="Solicitud inválida",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    example={"error": "Error inesperado"}
                )
            ),
            404: openapi.Response(
                description="Categoría no encontrada",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    example={"error": "Categoria no encontrada"}
                )
            )
        }
    )
    def get(self, request):
        categoria_id = request.GET.get("categoria_id")
        if not categoria_id:
            return JsonResponse({"error": "Error inesperado"}, status=HTTPStatus.BAD_REQUEST)

        try:
            Categoria.objects.filter(id=categoria_id).get()
        except Categoria.DoesNotExist:
            return JsonResponse({"error": "Categoria no encontrada"}, status=HTTPStatus.BAD_REQUEST)

        data = Ejercicio.objects.filter(
            categoria_id=categoria_id,
            nombre__icontains=request.GET.get('search', "")
        ).order_by('-id').all()

        datos_json = EjercicioSerializer(data, many=True)
        return JsonResponse({"data": datos_json.data}, status=HTTPStatus.OK)
