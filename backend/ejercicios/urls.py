from django.urls import path
from .views import Clase1, Clase2

urlpatterns = [
    path('ejercicios', Clase1.as_view()),
    path('ejercicios/<int:id>', Clase2.as_view()),
]
