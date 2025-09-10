// src/services/auth.js
import { httpPost, setAuthToken } from './http';

export async function register({ nombre, correo, password }) {
  // POST /api/v1/seguridad/registro
  const body = await httpPost('seguridad/registro', { nombre, correo, password });
  return body; // { message: 'Usuario registrado correctamente' } (201)
}

export async function login({ correo, password }) {
  // POST /api/v1/seguridad/login
  const body = await httpPost('seguridad/login', { correo, password });
  // body => { id, nombre, token }
  return body;
}

// Para que el resto de servicios usen el token
export function applyAuthToken(token) {
  setAuthToken(token);
}
