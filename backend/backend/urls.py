from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

# Swagger documentación
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentación de Rutinas de Gym - Backend",
        default_version='v1',
        description="API desarrollada para implementación del backend del sistema de ejercicios",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@myapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),

    # APIs
    path('api/v1/', include('categorias.urls')),
    path('api/v1/', include('ejercicios.urls')),         # ← reemplaza a recetas
    path('api/v1/', include('contacto.urls')),
    path('api/v1/', include('seguridad.urls')),
    path('api/v1/', include('ejercicios_helper.urls')),  # ← reemplaza a recetas_helper

    # Swagger / OpenAPI
    re_path(r'^documentacion(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('documentacion/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('documentacion/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Media (carpeta real: upload/)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
