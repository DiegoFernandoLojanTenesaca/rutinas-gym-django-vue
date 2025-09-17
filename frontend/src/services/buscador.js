import { httpGet } from './http';

export async function buscarEjercicios({ categoria_id, search = '' }) {
  const q = new URLSearchParams({ categoria_id, search }).toString();
  const { data } = await httpGet(`ejercicios-buscador?${q}`);
  return data;
}
