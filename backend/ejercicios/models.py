from django.db import models
from autoslug import AutoSlugField
from categorias.models import Categoria
from django.contrib.auth.models import User

class Ejercicio(models.Model):
    nombre = models.CharField(max_length=150, null=False)
    slug = AutoSlugField(populate_from='nombre', max_length=150, unique=True)
    tiempo = models.CharField(max_length=100, null=True, blank=True)
    foto = models.CharField(max_length=255, null=True, blank=True)  # guardamos el nombre del archivo
    descripcion = models.TextField()
    fecha = models.DateTimeField(auto_now=True)

    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=1)

    class Meta:
        db_table = "ejercicios"
        verbose_name = "Ejercicio"
        verbose_name_plural = "Ejercicios"

    def __str__(self):
        return self.nombre
