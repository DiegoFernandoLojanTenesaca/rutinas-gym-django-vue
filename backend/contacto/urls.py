from django.urls import path
from .views import Clase1

urlpatterns = [
    path('contacto', Clase1.as_view()),
]
