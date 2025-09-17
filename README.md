
# 🦁 Lion GYM — Django REST + Vue 3 (Vite)

Proyecto **full-stack** para gestionar **ejercicios y rutinas de gimnasio**, con **Django REST Framework + MySQL** en el backend y **Vue 3 + Vite** en el frontend.  
Incluye **autenticación JWT**, documentación **Swagger**, panel de usuario, buscador, categorías con portada automática y página de contacto.

---

## 📋 Contenido

- [Tecnologías](#-tecnologías)
- [Características](#-características)
- [Capturas](#-capturas)
- [Instalación y ejecución](#-instalación-y-ejecución)
- [Variables de entorno](#-variables-de-entorno)
- [Endpoints (extracto)](#-endpoints-extracto)
- [Autenticación (JWT)](#-autenticación-jwt)
- [Flujo de registro y verificación](#-flujo-de-registro-y-verificación)
- [Licencia](#-licencia)

---

## 🧰 Tecnologías

**Backend**
- Django 5 + Django REST Framework
- MySQL 8
- JWT (JSON Web Token) 
- Swagger (OpenAPI)

**Frontend**
- Vue 3 + Vite
- Pinia (estado) + Vue Router
- Fetch nativo para servicios

---

## ✨ Características

- **Explorar ejercicios** por nombre y categoría, con tarjetas y detalles por *slug*.
- **Categorías con “cover” automático**: si no hay imagen propia, toma una aleatoria de sus ejercicios.
- **Panel personal**: CRUD de ejercicios del usuario con filtros y orden.
- **Perfil**: edición de nombre, **correo bloqueado** y cambio de contraseña.
- **Contactos**: formulario funcional + mapa incrustado.
- **Acerca de**: sección informativa con KPIs y llamados a la acción.
- **Autenticación JWT** y verificación por correo (Mailtrap en dev).
- **Swagger** con documentación navegable.

---

## 🖼️ Capturas

<table>
  <tr>
    <td align="center">
      <img src="https://i.ibb.co/nqWSQfCr/inicio.png" alt="Inicio" width="420" />
      <br><sub><b>Inicio</b></sub>
    </td>
    <td align="center">
      <img src="https://i.ibb.co/B5K3zBfW/explorar.png" alt="Explorar" width="420" />
      <br><sub><b>Explorar ejercicios</b></sub>
    </td>
    <td align="center">
      <img src="https://i.ibb.co/KpYLBdKq/categoria.png" alt="Categorías" width="420" />
      <br><sub><b>Listado de categorías</b></sub>
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="https://i.ibb.co/8nSXrKBt/login.png" alt="Login" width="420" />
      <br><sub><b>Iniciar sesión</b></sub>
    </td>
    <td align="center">
      <img src="https://i.ibb.co/rGPZ5FbJ/cambiodadatos.png" alt="Perfil" width="420" />
      <br><sub><b>Perfil (correo bloqueado)</b></sub>
    </td>
    <td align="center">
      <img src="https://i.ibb.co/DDss5W6k/ejercicio.png" alt="Detalle de ejercicio" width="420" />
      <br><sub><b>Detalle de ejercicio</b></sub>
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="https://i.ibb.co/htbr5fk/final.png" alt="Panel / Cards" width="420" />
      <br><sub><b>Panel con tarjetas</b></sub>
    </td>
    <td></td>
    <td></td>
  </tr>
</table>

---

## 🚀 Instalación y ejecución

### 1) Backend

```bash
cd backend
python -m venv ../entorno            # opcional (venv fuera del backend)
source ../entorno/bin/activate       # Linux/macOS
# .\..\entorno\Scripts\activate  # Windows PowerShell

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

> Para build de producción: `npm run build` (sirve desde `dist/` con el servidor de tu preferencia).

---

## 🔧 Variables de entorno

**Backend – `settings.py` / `.env`**
- `DATABASES` → MySQL local
- `BASE_URL_FRONTEND` → URL a donde se redirige tras verificar cuenta (p.ej. `http://127.0.0.1:5173/login`)
- Mail (sandbox) → Mailtrap u otro
- CORS/CSRF → incluye el host del frontend

**Frontend – `.env`**
```
VITE_API_BASE=http://127.0.0.1:8000/api/v1/
```

---

## 🔗 Endpoints (extracto)

**Auth**
- `POST /api/v1/seguridad/registro` → Registro (envía email de verificación)
- `GET  /api/v1/seguridad/verificacion/<token>` → Verifica y **redirecciona** a `BASE_URL_FRONTEND`
- `POST /api/v1/seguridad/login` → Devuelve `{ id, nombre, token }`

**Ejercicios**
- `GET  /api/v1/ejercicios` → Listado (`?search=` opcional)
- `POST /api/v1/ejercicios` → Crear (**Bearer JWT**)
- `GET  /api/v1/ejercicios/<id>` → Detalle por ID
- `PUT  /api/v1/ejercicios/<id>` → Actualizar (**JWT**)
- `DELETE /api/v1/ejercicios/<id>` → Eliminar (**JWT**)

**Helpers ejercicios**
- `GET /api/v1/ejercicios-home` → 3 aleatorios para la Home
- `GET /api/v1/ejercicios/slug/<slug>` → Detalle por **slug**
- `GET /api/v1/ejercicios-panel/<user_id>` → Por usuario (**JWT**)
- `POST /api/v1/ejercicios/editar/foto` → Cambiar solo foto (**JWT**)
- `GET /api/v1/ejercicios-buscador?categoria_id=&search=` → Buscador

**Categorías**
- `GET /api/v1/categorias`
- `POST /api/v1/categorias` (crear)
- `GET /api/v1/categorias/<id>` (detalle)
- `PUT /api/v1/categorias/<id>` (actualizar)
- `DELETE /api/v1/categorias/<id>` (valida que no tenga ejercicios)

**Contacto**
- `POST /api/v1/contacto`

---

## 🔒 Autenticación (JWT)

Enviar en headers para endpoints protegidos:

```
Authorization: Bearer <token>
```

- Algoritmo: **HS512**
- Expiración: **1 día**
- El decorador `@logueado()` valida **formato**, **firma** y **expiración**.

---

## 🧭 Flujo de registro y verificación

1. Registro en `/seguridad/registro`.
2. Se envía un correo (Mailtrap en dev) con enlace:  
   `GET /api/v1/seguridad/verificacion/<token>`
3. Al abrirlo, el backend **activa** la cuenta y redirige a `BASE_URL_FRONTEND` (p.ej. `/login`).
4. Ya puede iniciar sesión en `/seguridad/login` y obtener el JWT.

> Si ves *“Error interno del servidor”* al verificar, revisa que `BASE_URL_FRONTEND` apunte a una URL válida.

---


## 📄 Licencia

Este proyecto está bajo la licencia incluida en `LICENSE`.
