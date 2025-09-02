from rest_framework.views import APIView
from django.http.response import JsonResponse
from http import HTTPStatus
from django.http import Http404
from django.utils.text import slugify
from rest_framework.permissions import AllowAny

from .models import Categoria
from .serializers import CategoriaSerializer

from ejercicios.models import Ejercicio

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class Clase1(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Obtener todas las categorías (grupos musculares/áreas) registradas",
        responses={
            200: openapi.Response(
                description="Lista de categorías",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "data": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "id": openapi.Schema(
                                        type=openapi.TYPE_INTEGER,
                                        description="ID de la categoría"
                                    ),
                                    "nombre": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="Nombre de la categoría (p.ej., Pecho, Espalda)"
                                    ),
                                    "slug": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="Slug generado automáticamente"
                                    ),
                                    "descripcion": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="Descripción opcional de la categoría",
                                    ),
                                }
                            )
                        )
                    },
                    example={
                        "data": [
                            {"id": 1, "nombre": "Pecho", "slug": "pecho", "descripcion": "Ejercicios para pectorales"},
                            {"id": 2, "nombre": "Espalda", "slug": "espalda", "descripcion": "Ejercicios para dorsales"}
                        ]
                    }
                )
            )
        }
    )
    def get(self, request):
        data = Categoria.objects.order_by('-id').all()
        datos_json = CategoriaSerializer(data, many=True)
        return JsonResponse({"data": datos_json.data}, status=HTTPStatus.OK)

    @swagger_auto_schema(
        operation_description="Agregar una nueva categoría (grupo muscular/área)",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre de la categoría'),
                'descripcion': openapi.Schema(type=openapi.TYPE_STRING, description='Descripción opcional'),
            },
            required=['nombre']
        ),
        responses={
            201: openapi.Response(
                description="Categoría creada exitosamente",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    example={"estado": "ok", "mensaje": "Se crea el registro exitosamente"}
                )
            ),
            400: openapi.Response(
                description="Error en los datos",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    example={"estado": "error", "mensaje": "El campo nombre es obligatorio"}
                )
            )
        }
    )
    def post(self, request):
        nombre = request.data.get("nombre")
        if nombre is None or not nombre:
            return JsonResponse(
                {"estado": "error", "mensaje": "El campo nombre es obligatorio"},
                status=HTTPStatus.BAD_REQUEST
            )
        try:
            Categoria.objects.create(
                nombre=nombre,
                descripcion=request.data.get("descripcion", None)
            )
            return JsonResponse(
                {"estado": "ok", "mensaje": "Se crea el registro exitosamente"},
                status=HTTPStatus.CREATED
            )
        except Exception:
            raise Http404


class Clase2(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Obtener una categoría específica por su ID",
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="ID de la categoría",
                type=openapi.TYPE_INTEGER
            )
        ],
        responses={
            200: openapi.Response(
                description="Datos de la categoría",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    example={
                        "data": {
                            "id": 1,
                            "nombre": "Pecho",
                            "slug": "pecho",
                            "descripcion": "Ejercicios para pectorales"
                        }
                    }
                )
            ),
            404: openapi.Response(
                description="Categoría no encontrada",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    example={"error": "Categoría no encontrada"}
                )
            )
        }
    )
    def get(self, request, id):
        try:
            data = Categoria.objects.filter(id=id).get()
            return JsonResponse(
                {
                    "data": {
                        "id": data.id,
                        "nombre": data.nombre,
                        "slug": data.slug,
                        "descripcion": data.descripcion
                    }
                },
                status=HTTPStatus.OK
            )
        except Categoria.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        operation_description="Editar una categoría por ID",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre de la categoría'),
                'descripcion': openapi.Schema(type=openapi.TYPE_STRING, description='Descripción opcional'),
            },
            required=['nombre']
        ),
        responses={
            200: openapi.Response(
                description="Categoría actualizado con éxito",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    example={"estado": "ok", "mensaje": "Se actualiza el registro exitosamente"}
                )
            ),
            400: openapi.Response(
                description="Error en los datos",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    example={"estado": "error", "mensaje": "El campo nombre es obligatorio"}
                )
            ),
            404: openapi.Response(
                description="Categoría no encontrada",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    example={"error": "Categoría no encontrada"}
                )
            )
        }
    )
    def put(self, request, id):
        nombre = request.data.get("nombre")
        if nombre is None or not nombre:
            return JsonResponse(
                {"estado": "error", "mensaje": "El campo nombre es obligatorio"},
                status=HTTPStatus.BAD_REQUEST
            )
        try:
            _ = Categoria.objects.filter(id=id).get()
            Categoria.objects.filter(id=id).update(
                nombre=nombre,
                slug=slugify(nombre),
                descripcion=request.data.get("descripcion", None)
            )
            return JsonResponse(
                {"estado": "ok", "mensaje": "Se actualiza el registro exitosamente"},
                status=HTTPStatus.OK
            )
        except Categoria.DoesNotExist:
            raise Http404
        except Exception:
            raise Http404

    @swagger_auto_schema(
        operation_description="Eliminar una categoría por ID (solo si no tiene ejercicios asociados)",
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="ID de la categoría",
                type=openapi.TYPE_INTEGER
            )
        ],
        responses={
            200: openapi.Response(
                description="Categoría eliminada con éxito",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    example={"estado": "ok", "mensaje": "Se elimina el registro exitosamente"}
                )
            ),
            400: openapi.Response(
                description="No se puede eliminar la categoría (tiene ejercicios asociados)",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    example={"estado": "error", "mensaje": "No se puede eliminar la categoría porque tiene ejercicios asociados"}
                )
            ),
            404: openapi.Response(
                description="Categoría no encontrada",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    example={"error": "Categoría no encontrada"}
                )
            )
        }
    )
    def delete(self, request, id):
        try:
            _ = Categoria.objects.filter(id=id).get()
        except Categoria.DoesNotExist:
            raise Http404

        # Bloquear borrado si hay ejercicios asociados
        if Ejercicio.objects.filter(categoria_id=id).exists():
            return JsonResponse(
                {"estado": "error", "mensaje": "No se puede eliminar la categoría porque tiene ejercicios asociados"},
                status=HTTPStatus.BAD_REQUEST
            )

        Categoria.objects.filter(id=id).delete()
        return JsonResponse(
            {"estado": "ok", "mensaje": "Se elimina el registro exitosamente"},
            status=HTTPStatus.OK)
