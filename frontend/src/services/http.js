// src/services/http.js
const RAW = import.meta.env.VITE_API_BASE;
const BASE = RAW.replace(/\/+$/, ''); // sin slash final

let _token = null;

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
  try { body = await res.json(); } catch (_) { /* ignore parse error */ }
  if (!res.ok) {
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
