
# 🏋️‍♂️ Rutinas Gym - Backend Django & Frontend Vue

Proyecto fullstack para gestionar **rutinas de gimnasio**, con un
backend en **Django REST Framework** y un frontend en **Vue.js**.

## 🚀 Tecnologías

-   **Backend**: Django 5 + Django REST Framework + MySQL
-   **Frontend**: Vue.js + Vite
-   **Auth**: JWT con `python-jose`
-   **Documentación**: Swagger (drf-yasg)

## ⚙️ Requisitos

-   Python 3.10+
-   Node.js 18+
-   MySQL 8+

## 📦 Instalación Backend

    cd backend  
    pip install -r requirements.txt  
    python manage.py migrate  
    python manage.py runserver  

Backend corre en:\
👉 http://127.0.0.1:8000/

Swagger docs en:\
👉 http://127.0.0.1:8000/documentacion/

## 🎨 Instalación Frontend

    cd frontend  
    npm install  
    npm run dev  

Frontend corre en:\
👉 http://127.0.0.1:5173/

## 📖 Endpoints principales

-   `POST /api/v1/seguridad/registro` → Registro de usuario
-   `POST /api/v1/seguridad/login` → Login y obtención de token
-   `GET /api/v1/categorias` → Listado de categorías
-   `POST /api/v1/ejercicios` → Crear ejercicio (requiere JWT)

## 🛡️ Autenticación

En los endpoints protegidos, enviar el JWT en headers:

    Authorization: Bearer <tu_token>

------------------------------------------------------------------------
