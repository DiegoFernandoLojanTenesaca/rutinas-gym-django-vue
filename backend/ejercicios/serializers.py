from rest_framework import serializers
from .models import Ejercicio
import os

class EjercicioSerializer(serializers.ModelSerializer):
    categoria = serializers.ReadOnlyField(source='categoria.nombre')
    fecha = serializers.DateTimeField(format="%d/%m/%Y")
    imagen = serializers.SerializerMethodField()
    user = serializers.ReadOnlyField(source='user.first_name')

    class Meta:
        model = Ejercicio
        fields = (
            "id", "nombre", "slug", "tiempo", "descripcion", "fecha",
            "categoria", "categoria_id", "imagen", "user_id", "user"
        )

    def get_imagen(self, obj):
        # BASE_URL + upload/ejercicios/<archivo>
        base_url = os.getenv("BASE_URL", "http://127.0.0.1:8000/")
        if not base_url.endswith("/"):
            base_url += "/"
        if obj.foto:
            return f"{base_url}upload/ejercicios/{obj.foto}"
        return None
