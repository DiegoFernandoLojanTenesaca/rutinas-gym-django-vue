
# 🦁 Lion GYM — Django REST + Vue 3 (Vite)

Proyecto full‑stack para gestionar **ejercicios y rutinas de gimnasio**, con **Django REST Framework + MySQL** en el backend y **Vue 3 + Vite** en el frontend. Incluye autenticación **JWT**, documentación **Swagger**.

---

## 🚀 Tecnologías principales

**Backend**
- Django 5 + Django REST Framework
- MySQL 8
- `JWT` (JSON Web Token) 
- `Swagger` (OpenAPI)

**Frontend**
- Vue 3 + Vite
- Pinia (estado) + Vue Router
- Fetch nativo para servicios

---

## 🧰 Instalación y ejecución

### 1) Backend

```bash
cd backend
python -m venv ../entorno      # opcional, crea venv fuera del backend

pip install -r ../requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```
- API: **http://127.0.0.1:8000/**
- Swagger: **http://127.0.0.1:8000/documentacion/**


### 2) Frontend

```bash
cd frontend
npm install
npm run dev -- --host
```
- Frontend: **http://127.0.0.1:5173/**

---

## 🔗 Endpoints relevantes (extracto)

- **Auth**
  - `POST /api/v1/seguridad/registro` → Registro de usuario (envía email con enlace de verificación)
  - `GET  /api/v1/seguridad/verificacion/<token>` → Verifica cuenta y **redirecciona** a `BASE_URL_FRONTEND`
  - `POST /api/v1/seguridad/login` → Devuelve `{ id, nombre, token }`

- **Ejercicios**
  - `GET  /api/v1/ejercicios` → Listado (con `?search=` opcional)
  - `POST /api/v1/ejercicios` → Crear (requiere **Bearer JWT** y campos válidos)
  - `GET  /api/v1/ejercicios/<id>` → Detalle por ID
  - `PUT /api/v1/ejercicios/<id>` → Actualizar (requiere JWT)
  - `DELETE /api/v1/ejercicios/<id>` → Eliminar (requiere JWT)

- **Helpers ejercicios**
  - `GET /api/v1/ejercicios-home` → 3 ejercicios aleatorios para la Home
  - `GET /api/v1/ejercicios/slug/<slug>` → Detalle por **slug**
  - `GET /api/v1/ejercicios-panel/<user_id>` → Ejercicios por usuario (requiere JWT)
  - `POST /api/v1/ejercicios/editar/foto` → Cambiar solo foto (requiere JWT)
  - `GET /api/v1/ejercicios-buscador?categoria_id=&search=` → Buscador

- **Categorías**
  - `GET /api/v1/categorias`
  - `POST /api/v1/categorias` (crear)
  - `GET /api/v1/categorias/<id>` (detalle)
  - `PUT /api/v1/categorias/<id>` (actualizar)
  - `DELETE /api/v1/categorias/<id>` (eliminar; valida que no tenga ejercicios)

- **Contacto**
  - `POST /api/v1/contacto`

---

## 🔒 Autenticación (JWT)

Enviar en headers para endpoints protegidos:
```
Authorization: Bearer <token>
```

El token se firma con **HS512** y expira en **1 día**. El decorador `@logueado()` del backend valida **formato**, **firma** y **expiración**.

---

## 🧭 Flujo de registro y verificación

1. El usuario se registra en `/seguridad/registro`.
2. Se envía email (Mailtrap sandbox) con un enlace de verificación:  
   `GET /api/v1/seguridad/verificacion/<token>`
3. Al hacer click, el backend **activa** la cuenta y redirige a `BASE_URL_FRONTEND` (por ejemplo `/login` del frontend).  
4. Ya puede iniciar sesión en `/seguridad/login` y obtener el JWT.

> Si al abrir el enlace ves *“Error interno del servidor”*, revisa que `BASE_URL_FRONTEND` apunte a una URL válida.
---

## 🧪 Prueba rápida

1. **Home**: debe mostrar “Ejercicios destacados” (3 aleatorios desde `/ejercicios-home`).  
2. **Detalle**: desde Home, click en un ejercicio → `/ejercicio/:slug` (pide `/ejercicios/slug/<slug>`).  
3. **Registro**: crea un usuario, verifica en Mailtrap el email y haz click.  
4. **Login**: haz login; el frontend guarda el token (Pinia + `localStorage`).  
5. 

---

## 🧯 Troubleshooting

- **“You’re accessing the development server over HTTPS…”**  
  Usa `http://` (no `https://`) con el servidor de desarrollo de Django.
- **CORS bloqueado**  
  Verifica `CORS_ORIGIN_WHITELIST` y `VITE_API_BASE`.
- **Imágenes no cargan**  
  Asegúrate que `BASE_URL` apunte al backend correcto y que la ruta `MEDIA_URL=/upload/` esté servida (Django `static()` en `urls.py`).
- **Enlace de verificación falla**  
  Revisa que `BASE_URL_FRONTEND` sea accesible desde el navegador que abre el email.

---

## 📄 Licencia 
Este proyecto está bajo la licencia incluida en `LICENSE`.
