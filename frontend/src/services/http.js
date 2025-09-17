// src/services/http.js
const RAW = import.meta.env.VITE_API_BASE;
const BASE = RAW.replace(/\/+$/, ''); // sin slash final

let _token = null;

// añade arriba (estado global simple)
let _onUnauthorized = null;
export function setOnUnauthorized(fn) { _onUnauthorized = fn; }

// Permite que otros módulos configuren el token global
export function setAuthToken(token) {
  _token = token || null;
}

function buildUrl(path) {
  const clean = String(path).replace(/^\/+/, ''); // sin slash inicial
  // Asegura prefijo /api/v1/
  return `${BASE}/api/v1/${clean.replace(/^api\/v1\/?/, '')}`;
}

// Pequeña ayuda para respuestas no-2xx
async function parseOrThrow(res) {
  let body = null;
  try { body = await res.json(); } catch (_) { /* ignore */ }

  if (!res.ok) {
    // Manejo centralizado de 401
    if (res.status === 401 && typeof _onUnauthorized === 'function') {
      try { _onUnauthorized(); } catch (_) {}
    }
    const msg = (body && (body.error || body.mensaje || body.message)) || 'Error de red';
    const err = new Error(msg);
    err.status = res.status;
    err.body = body;
    throw err;
  }
  return body;
}


export async function httpGet(path) {
  const res = await fetch(buildUrl(path), {
    method: 'GET',
    headers: {
      ...( _token ? { Authorization: `Bearer ${_token}` } : {} ),
    },
  });
  return parseOrThrow(res);
}

export async function httpPost(path, data) {
  const res = await fetch(buildUrl(path), {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...( _token ? { Authorization: `Bearer ${_token}` } : {} ),
    },
    body: JSON.stringify(data),
  });
  return parseOrThrow(res);
}

// --- AÑADIR DEBAJO DE httpPost ---
export async function httpPut(path, data) {
  const res = await fetch(buildUrl(path), {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      ...( _token ? { Authorization: `Bearer ${_token}` } : {} ),
    },
    body: JSON.stringify(data),
  });
  return parseOrThrow(res);
}

export async function httpDelete(path) {
  const res = await fetch(buildUrl(path), {
    method: 'DELETE',
    headers: {
      ...( _token ? { Authorization: `Bearer ${_token}` } : {} ),
    },
  });
  return parseOrThrow(res);
}

// Para subir archivos (foto)
export async function httpPostForm(path, formData) {
  const res = await fetch(buildUrl(path), {
    method: 'POST',
    headers: {
      ...( _token ? { Authorization: `Bearer ${_token}` } : {} ),
      // NO pongas Content-Type: fetch lo setea con boundary
    },
    body: formData,
  });
  return parseOrThrow(res);
}
