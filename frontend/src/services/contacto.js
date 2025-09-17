import { httpPost } from './http';

export async function enviarContacto({ nombre, correo, telefono, mensaje }) {
  return await httpPost('contacto', { nombre, correo, telefono, mensaje });
}
