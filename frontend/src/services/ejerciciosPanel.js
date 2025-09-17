import { httpGet, httpPost, httpPut, httpDelete, httpPostForm } from './http';

// Lista ejercicios del usuario autenticado
export async function listByUser(userId) {
  const { data } = await httpGet(`ejercicios-panel/${userId}`);
  return data;
}

// Crear ejercicio (sin foto)
export async function createEjercicio(payload) {
  // payload: {nombre, tiempo, descripcion, categoria_id, foto: File}
  // La API /ejercicios (POST) EXIGE foto en el mismo request, así que usamos form:
  const fd = new FormData();
  fd.append('nombre', payload.nombre);
  fd.append('tiempo', payload.tiempo);
  fd.append('descripcion', payload.descripcion);
  fd.append('categoria_id', payload.categoria_id);
  fd.append('foto', payload.foto);
  return await httpPostForm('ejercicios', fd);
}

// Actualizar ejercicio (sin cambiar foto)
export async function updateEjercicio(id, payload) {
  // {nombre, tiempo, descripcion, categoria_id}
  return await httpPut(`ejercicios/${id}`, payload);
}

// Eliminar
export async function deleteEjercicio(id) {
  return await httpDelete(`ejercicios/${id}`);
}

// Actualizar SOLO la foto
export async function updateFoto(id, file) {
  const fd = new FormData();
  fd.append('id', id);
  fd.append('foto', file);
  return await httpPostForm('ejercicios/editar/foto', fd);
}
