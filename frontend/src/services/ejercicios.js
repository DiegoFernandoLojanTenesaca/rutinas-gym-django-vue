// src/services/ejercicios.js
const RAW = import.meta.env.VITE_API_BASE;
const BASE = RAW.replace(/\/+$/, '')

function url(path) {
  const clean = String(path).replace(/^\/+/, '')
  return `${BASE}/api/v1/${clean.replace(/^api\/v1\/?/, '')}`
}

export async function getEjerciciosHome() {
  const endpoint = url('ejercicios-home')
  console.log('[Home] GET:', endpoint)
  const res = await fetch(endpoint)
  if (!res.ok) throw new Error('No se pudieron cargar ejercicios')
  const { data } = await res.json()
  return data
}

export async function getEjercicioPorSlug(slug) {
  const endpoint = url(`ejercicios/slug/${slug}`)
  console.log('[Detalle] GET:', endpoint)
  const res = await fetch(endpoint)
  if (!res.ok) throw new Error('No se pudo cargar el ejercicio')
  const { data } = await res.json()
  return data
}
