from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home_inicio(request):
    return HttpResponse("Hola, Mundo! Esta es la página de inicio.")
