import { httpGet } from './http';

export async function getCategorias() {
  const { data } = await httpGet('categorias');
  return data; // [{id, nombre, slug, ...}]
}
