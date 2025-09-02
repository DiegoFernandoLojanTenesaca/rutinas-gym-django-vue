from django.urls import path
from .views import Clase1, Clase2, Clase3, Clase4, Clase5

urlpatterns = [
    path('ejercicios/editar/foto', Clase1.as_view()),
    path('ejercicios/slug/<str:slug>', Clase2.as_view()),
    path('ejercicios-home', Clase3.as_view()),
    path('ejercicios-panel/<int:id>', Clase4.as_view()),
    path('ejercicios-buscador', Clase5.as_view()),
]
