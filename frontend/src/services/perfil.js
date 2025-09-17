import { httpGet, httpPut } from './http';

// GET datos del usuario autenticado
export async function getPerfil() {
  // Ajusta si tu backend usa otro endpoint, p.ej. 'seguridad/perfil'
  const { data } = await httpGet('usuarios/me');
  return data; // { id, nombre, correo }
}

// PUT actualizar nombre/correo
export async function updatePerfil(payload) {
  // payload: { nombre, correo }
  return await httpPut('usuarios/me', payload);
}

// PUT cambiar contraseña
export async function cambiarPassword({ actual, nueva }) {
  // algunos backends usan POST; ajusta si hace falta
  return await httpPut('usuarios/me/password', { actual, nueva });
}
