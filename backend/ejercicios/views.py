from rest_framework.views import APIView
from django.http.response import JsonResponse
from http import HTTPStatus
from django.http import Http404
from django.utils.text import slugify
from rest_framework.permissions import AllowAny
from django.utils.dateformat import DateFormat
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.conf import settings

import os
from jose import jwt

from .models import Ejercicio
from categorias.models import Categoria
from .serializers import EjercicioSerializer
from seguridad.decorators import logueado

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class Clase1(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Obtener todos los ejercicios registrados",
        manual_parameters=[
            openapi.Parameter(
                name="search",
                in_=openapi.IN_QUERY,
                description="Texto a buscar en el nombre del ejercicio",
                type=openapi.TYPE_STRING,
                required=False
            )
        ],
        responses={
            200: openapi.Response(
                description="Lista de ejercicios",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "data": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                                    "nombre": openapi.Schema(type=openapi.TYPE_STRING),
                                    "slug": openapi.Schema(type=openapi.TYPE_STRING),
                                    "tiempo": openapi.Schema(type=openapi.TYPE_STRING),
                                    "descripcion": openapi.Schema(type=openapi.TYPE_STRING),
                                    "fecha": openapi.Schema(type=openapi.TYPE_STRING),
                                    "categoria": openapi.Schema(type=openapi.TYPE_STRING),
                                    "categoria_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                                    "imagen": openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                    "user_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                                    "user": openapi.Schema(type=openapi.TYPE_STRING),
                                }
                            )
                        )
                    },
                    example={
                        "data": [
                            {
                                "id": 1,
                                "nombre": "Press banca",
                                "slug": "press-banca",
                                "tiempo": "3x10",
                                "descripcion": "Ejercicio de pecho con barra",
                                "fecha": "01/09/2025",
                                "categoria": "Pecho",
                                "categoria_id": 2,
                                "imagen": "http://127.0.0.1:8000/upload/ejercicios/press.png",
                                "user_id": 1,
                                "user": "Diego"
                            }
                        ]
                    }
                )
            )
        }
    )
    def get(self, request):
        qs = Ejercicio.objects.order_by('-id')
        search = request.GET.get("search")
        if search:
            qs = qs.filter(nombre__icontains=search)

        datos_json = EjercicioSerializer(qs, many=True)
        return JsonResponse({"data": datos_json.data}, status=HTTPStatus.OK)

    @logueado()
    @swagger_auto_schema(
        operation_description="Crear un nuevo ejercicio",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del ejercicio'),
                'tiempo': openapi.Schema(type=openapi.TYPE_STRING, description='Tiempo/series de ejecución'),
                'descripcion': openapi.Schema(type=openapi.TYPE_STRING, description='Descripción del ejercicio'),
                'categoria_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la categoría'),
                'foto': openapi.Schema(type=openapi.TYPE_FILE, description='Foto del ejercicio'),
            },
            required=['nombre', 'tiempo', 'descripcion', 'categoria_id', 'foto']
        ),
        responses={
            201: openapi.Response(
                description="Ejercicio creado con éxito",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    example={"estado": "ok", "mensaje": "Ejercicio creado con éxito"}
                )
            ),
            400: openapi.Response(
                description="Error en los datos enviados",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    example={"error": "El campo nombre es obligatorio"}
                )
            ),
            401: openapi.Response(
                description="No autorizado",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    example={"error": "Token inválido o expirado"}
                )
            ),
        }
    )
    def post(self, request):
        if not request.data.get("nombre"):
            return JsonResponse({"error": "El campo nombre es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        if not request.data.get("tiempo"):
            return JsonResponse({"error": "El campo tiempo es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        if not request.data.get("descripcion"):
            return JsonResponse({"error": "El campo descripcion es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        if not request.data.get("categoria_id"):
            return JsonResponse({"error": "El campo categoria_id es obligatorio"}, status=HTTPStatus.BAD_REQUEST)

        # Validar categoría
        try:
            Categoria.objects.get(id=request.data["categoria_id"])
        except Categoria.DoesNotExist:
            return JsonResponse({"error": "La categoría no existe en la base de datos"}, status=HTTPStatus.BAD_REQUEST)

        # No duplicados por nombre
        if Ejercicio.objects.filter(nombre=request.data.get("nombre")).exists():
            return JsonResponse({"error": f"Ya existe un ejercicio con el nombre {request.data['nombre']}"}, status=HTTPStatus.BAD_REQUEST)

        # Subir imagen a MEDIA_ROOT/ejercicios/<archivo>
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, "ejercicios"))
        try:
            ext = os.path.splitext(str(request.FILES['foto']))[1]
            foto = f"{timezone.now().timestamp()}{ext}"
        except Exception:
            return JsonResponse({"error": "Se debe adjuntar una imagen en el campo 'foto'"}, status=HTTPStatus.BAD_REQUEST)

        try:
            fs.save(foto, request.FILES['foto'])
        except Exception:
            return JsonResponse({"error": "Se produjo un error al intentar subir el archivo"}, status=HTTPStatus.BAD_REQUEST)

        # Decodificar token
        try:
            header = (request.headers.get('Authorization') or "").split(" ")
            token = header[1] if len(header) == 2 else ""
            resuelto = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS512"])
        except Exception:
            return JsonResponse({"error": "Token inválido o expirado"}, status=HTTPStatus.UNAUTHORIZED)

        # Crear registro
        try:
            Ejercicio.objects.create(
                nombre=request.data['nombre'],
                tiempo=request.data['tiempo'],
                descripcion=request.data['descripcion'],
                categoria_id=request.data['categoria_id'],
                fecha=timezone.now(),
                foto=foto,
                user_id=resuelto['id']
            )
            return JsonResponse({"estado": "ok", "mensaje": "Ejercicio creado con éxito"}, status=HTTPStatus.CREATED)
        except Exception:
            raise Http404("No se pudo crear el ejercicio")


class Clase2(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Obtener un ejercicio específico por su ID",
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="ID del ejercicio",
                type=openapi.TYPE_INTEGER
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
                            "nombre": "Press banca",
                            "slug": "press-banca",
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
    def get(self, request, id):
        try:
            data = Ejercicio.objects.filter(id=id).get()
            return JsonResponse(
                {"data": {
                    "id": data.id,
                    "nombre": data.nombre,
                    "slug": data.slug,
                    "tiempo": data.tiempo,
                    "descripcion": data.descripcion,
                    "fecha": DateFormat(data.fecha).format('d/m/Y'),
                    "categoria": data.categoria.nombre,
                    "categoria_id": data.categoria_id,
                    "imagen": f"{os.getenv('BASE_URL', 'http://127.0.0.1:8000/')}" \
                              f"{'' if os.getenv('BASE_URL','').endswith('/') else '/'}" \
                              f"upload/ejercicios/{data.foto}" if data.foto else None,
                    "user_id": data.user_id,
                    "user": data.user.first_name
                }},
                status=HTTPStatus.OK
            )
        except Ejercicio.DoesNotExist:
            return JsonResponse({"error": "Ejercicio no encontrado"}, status=HTTPStatus.NOT_FOUND)

    @logueado()
    @swagger_auto_schema(
        operation_description="Actualizar un ejercicio existente",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre del ejercicio'),
                'tiempo': openapi.Schema(type=openapi.TYPE_STRING, description='Tiempo/series de ejecución'),
                'descripcion': openapi.Schema(type=openapi.TYPE_STRING, description='Descripción del ejercicio'),
                'categoria_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la categoría'),
                # Nota: la foto suele actualizarse con un endpoint específico; aquí la ignoramos en PUT
            },
            required=['nombre', 'tiempo', 'descripcion', 'categoria_id']
        ),
        responses={
            200: openapi.Response(
                description="Ejercicio actualizado con éxito",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    example={"estado": "ok", "mensaje": "Ejercicio actualizado con éxito"}
                )
            ),
            400: openapi.Response(
                description="Error en los datos enviados",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    example={"error": "El campo nombre es obligatorio"}
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
    def put(self, request, id):
        try:
            Ejercicio.objects.filter(id=id).get()
        except Ejercicio.DoesNotExist:
            return JsonResponse({"error": "Ejercicio no encontrado"}, status=HTTPStatus.NOT_FOUND)

        if not request.data.get("nombre"):
            return JsonResponse({"error": "El campo nombre es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        if not request.data.get("tiempo"):
            return JsonResponse({"error": "El campo tiempo es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        if not request.data.get("descripcion"):
            return JsonResponse({"error": "El campo descripcion es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        if not request.data.get("categoria_id"):
            return JsonResponse({"error": "El campo categoria_id es obligatorio"}, status=HTTPStatus.BAD_REQUEST)

        try:
            Categoria.objects.get(id=request.data["categoria_id"])
        except Categoria.DoesNotExist:
            return JsonResponse({"error": "La categoría no existe en la base de datos"}, status=HTTPStatus.BAD_REQUEST)

        try:
            Ejercicio.objects.filter(id=id).update(
                nombre=request.data['nombre'],
                slug=slugify(request.data['nombre']),
                tiempo=request.data['tiempo'],
                descripcion=request.data['descripcion'],
                categoria_id=request.data['categoria_id']
            )
            return JsonResponse({"estado": "ok", "mensaje": "Ejercicio actualizado con éxito"}, status=HTTPStatus.OK)
        except Exception:
            return JsonResponse({"error": "Se produjo un error al intentar actualizar el ejercicio"}, status=HTTPStatus.BAD_REQUEST)

    @logueado()
    @swagger_auto_schema(
        operation_description="Eliminar un ejercicio existente",
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="ID del ejercicio",
                type=openapi.TYPE_INTEGER
            )
        ],
        responses={
            200: openapi.Response(
                description="Ejercicio eliminado con éxito",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    example={"estado": "ok", "mensaje": "Ejercicio eliminado con éxito"}
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
    def delete(self, request, id):
        try:
            data = Ejercicio.objects.filter(id=id).get()
        except Ejercicio.DoesNotExist:
            return JsonResponse({"error": "Ejercicio no encontrado"}, status=HTTPStatus.NOT_FOUND)

        # Borrar archivo físico de forma segura: MEDIA_ROOT/ejercicios/<foto>
        if data.foto:
            file_path = os.path.join(settings.MEDIA_ROOT, "ejercicios", data.foto)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception:
                    # no interrumpas si el archivo no se puede borrar
                    pass

        Ejercicio.objects.filter(id=id).delete()
        return JsonResponse({"estado": "ok", "mensaje": "Ejercicio eliminado con éxito"}, status=HTTPStatus.OK)
