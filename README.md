
# 🦁 Lion GYM — Django REST + Vue 3 (Vite)

> Plataforma full‑stack para **descubrir, crear y organizar rutinas de gimnasio**.  
> Backend **Django REST + MySQL**, frontend **Vue 3 + Vite**, autenticación **JWT**, y documentación **Swagger**.

<p align="left">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white">
  <img alt="Django" src="https://img.shields.io/badge/Django-5-092E20?logo=django&logoColor=white">
  <img alt="DRF" src="https://img.shields.io/badge/DRF-3.x-red">
  <img alt="MySQL" src="https://img.shields.io/badge/MySQL-8-4479A1?logo=mysql&logoColor=white">
  <img alt="Vue" src="https://img.shields.io/badge/Vue-3-42b883?logo=vue.js&logoColor=white">
  <img alt="Vite" src="https://img.shields.io/badge/Vite-5-646CFF?logo=vite&logoColor=white">
</p>

---

## ✨ Características clave

- **Explorar ejercicios** por nombre y por **categorías** (grid responsiva).  
- **Detalle de ejercicio** por *slug* con grupos musculares, series/tiempo y foto.  
- **Categorías con cover**: si no tienen imagen propia, se **toma aleatoria** de los ejercicios de esa categoría.  
- **Panel del usuario**: CRUD de ejercicios personales, filtros (categoría, texto), orden y paginación.  
- **Perfil**: edición de nombre y **bloqueo de email** (solo lectura), cambio de contraseña con validaciones.  
- **Autenticación JWT** (login/registro) con **verificación por correo**.  
- **Contacto**: formulario + validaciones y mapa (Loja, Ecuador).  
- **UI limpia** y consistente con tarjetas, sombras suaves y foco accesible.

---

## 🧱 Arquitectura (alto nivel)

```
Frontend (Vue 3 + Vite + Pinia)
   │
   ├── Servicios fetch nativo (Bearer JWT)
   │
Backend (Django REST Framework) ── MySQL 8
   ├── /ejercicios, /categorias, /seguridad, /contacto
   └── JWT HS512 (24h) + Swagger
```

---

## 🧰 Requisitos

- **Python** 3.11+
- **Node.js** 18+ y **npm**
- **MySQL** 8 (local o contenedor)

---

## ⚙️ Configuración rápida

### 1) Backend

```bash
cd backend
# (opcional) entorno virtual
python -m venv ../entorno && source ../entorno/bin/activate  # Windows: ..\entorno\Scripts\activate

# dependencias (el repo incluye requirements en la raíz)
pip install -r ../requirements.txt

# migraciones y arranque
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

- API base: **http://127.0.0.1:8000/**
- Swagger: **http://127.0.0.1:8000/documentacion/**

**Variables de configuración recomendadas** (en tu `settings.py` o env):
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`  
- `SECRET_KEY`  
- `BASE_URL_FRONTEND` (por ej. `http://127.0.0.1:5173`)  
- Credenciales de correo (sandbox tipo Mailtrap) para verificación.

---

### 2) Frontend

```bash
cd frontend
npm install
# crea .env.local con la URL del backend:
# VITE_API_BASE=http://127.0.0.1:8000/api/v1
npm run dev -- --host
```

- App: **http://127.0.0.1:5173/**

---

## 🔗 Endpoints principales (extracto)

**Auth**
- `POST /api/v1/seguridad/registro` — registro (envía email con enlace)
- `GET  /api/v1/seguridad/verificacion/<token>` — activa y **redirige** a `BASE_URL_FRONTEND`
- `POST /api/v1/seguridad/login` — devuelve `{ id, nombre, token }`

**Ejercicios**
- `GET  /api/v1/ejercicios?search=…`
- `GET  /api/v1/ejercicios/slug/<slug>`
- `POST /api/v1/ejercicios` (JWT)
- `PUT  /api/v1/ejercicios/<id>` (JWT)
- `DELETE /api/v1/ejercicios/<id>` (JWT)
- `GET  /api/v1/ejercicios-home` — 3 aleatorios para la Home
- `GET  /api/v1/ejercicios-buscador?categoria_id=&search=` — listado por categoría/busca
- `GET  /api/v1/ejercicios-panel/<user_id>` — del usuario (JWT)

**Categorías**
- `GET  /api/v1/categorias`
- `POST /api/v1/categorias` (JWT)
- `GET  /api/v1/categorias/<id>`
- `PUT  /api/v1/categorias/<id>` (JWT)
- `DELETE /api/v1/categorias/<id>` (JWT; valida que no tenga ejercicios)

**Contacto**
- `POST /api/v1/contacto`

---

## 👀 Capturas (UI)

> Tamaño reducido para mejor lectura. Haz clic en cualquier imagen para verla completa.

<table>
  <tr>
    <td align="center">
      <a href="https://i.ibb.co/nqWSQfCr/inicio.png" target="_blank">
        <img src="https://i.ibb.co/nqWSQfCr/inicio.png" width="420" alt="Inicio">
      </a>
      <br><sub><b>Inicio</b> — héroe con CTA</sub>
    </td>
    <td align="center">
      <a href="https://i.ibb.co/8nSXrKBt/login.png" target="_blank">
        <img src="https://i.ibb.co/8nSXrKBt/login.png" width="420" alt="Login">
      </a>
      <br><sub><b>Autenticación</b> — login</sub>
    </td>
  </tr>
  <tr>
    <td align="center">
      <a href="https://i.ibb.co/TD98wQ2r/REGISTRO.png" target="_blank">
        <img src="https://i.ibb.co/TD98wQ2r/REGISTRO.png" width="420" alt="Registro">
      </a>
      <br><sub><b>Registro</b> — creación de cuenta</sub>
    </td>
    <td align="center">
      <a href="https://i.ibb.co/rGPZ5FbJ/cambiodadatos.png" target="_blank">
        <img src="https://i.ibb.co/rGPZ5FbJ/cambiodadatos.png" width="420" alt="Perfil">
      </a>
      <br><sub><b>Perfil</b> — datos y cambio de contraseña</sub>
    </td>
  </tr>
  <tr>
    <td align="center">
      <a href="https://i.ibb.co/explorar.png" target="_blank">
        <img src="https://i.ibb.co/B5K3zBfW/explorar.png" width="420" alt="Explorar">
      </a>
      <br><sub><b>Explorar</b> — listado con filtros</sub>
    </td>
    <td align="center">
      <a href="https://i.ibb.co/XZK4JJqR/busqueda.png" target="_blank">
        <img src="https://i.ibb.co/XZK4JJqR/busqueda.png" width="420" alt="Búsqueda">
      </a>
      <br><sub><b>Búsqueda</b> — resultados</sub>
    </td>
  </tr>
  <tr>
    <td align="center">
      <a href="https://i.ibb.co/KpYLBdKq/categoria.png" target="_blank">
        <img src="https://i.ibb.co/KpYLBdKq/categoria.png" width="420" alt="Categorías">
      </a>
      <br><sub><b>Categorías</b> — grid con cover automático</sub>
    </td>
    <td align="center">
      <a href="https://i.ibb.co/DDss5W6k/ejercicio.png" target="_blank">
        <img src="https://i.ibb.co/DDss5W6k/ejercicio.png" width="420" alt="Detalle">
      </a>
      <br><sub><b>Detalle</b> — ejercicio por slug</sub>
    </td>
  </tr>
  <tr>
    <td align="center">
      <a href="https://i.ibb.co/htbr5fk/final.png" target="_blank">
        <img src="https://i.ibb.co/htbr5fk/final.png" width="420" alt="Footer">
      </a>
      <br><sub><b>Footer</b> — suscripción y enlaces</sub>
    </td>
    <td align="center">
      <a href="https://i.ibb.co/B5K3zBfW/explorar.png" target="_blank">
        <img src="https://i.ibb.co/B5K3zBfW/explorar.png" width="420" alt="Explorar (extra)">
      </a>
      <br><sub><b>Explorar</b> — tarjetas responsivas</sub>
    </td>
  </tr>
</table>

---

## 🗂️ Estructura (resumen)

```
backend/
  seguridad/      ← auth, verificación, JWT
  ejercicios/     ← ejercicios (slug), helpers home/buscador
  categorias/     ← CRUD categorías
  contacto/       ← endpoint de contacto
frontend/
  src/
    views/        ← páginas (Home, About, Categorías, Panel, etc.)
    services/     ← fetch nativo (http, ejercicios, categorías, perfil…)
    stores/       ← Pinia (auth)
```

---

## 🔒 Autenticación

Enviar el token en los endpoints protegidos:

```
Authorization: Bearer <token>
```

- Firma **HS512**
- Expira en **24h**
- Decorador `@logueado()` valida formato, firma y expiración.

---

## 📜 Licencia

Este proyecto está bajo la licencia incluida en `LICENSE`.
