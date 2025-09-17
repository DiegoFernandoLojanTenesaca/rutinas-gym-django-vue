<template>
  <section class="contact_section layout_padding sub_page">
    <div class="container">
      <div class="heading_container"><h2>Contáctanos</h2></div>

      <div class="layout_padding2-top">
        <div class="row">
          <!-- Formulario -->
          <div class="col-md-6">
            <form @submit.prevent="onEnviar" novalidate>
              <div class="contact_form-container">
                <div>
                  <div>
                    <input v-model.trim="cNombre" type="text" placeholder="Nombre" required />
                  </div>
                  <div>
                    <input v-model.trim="cCorreo" type="email" placeholder="Correo electrónico" required />
                  </div>
                  <div>
                    <input v-model.trim="cTelefono" type="tel" placeholder="Teléfono (ej. +593 9xxxxxxx)" required />
                  </div>
                  <div class="mt-5">
                    <textarea v-model.trim="cMensaje" rows="4" placeholder="Mensaje" required style="width:100%;border:none;border-bottom:.8px solid #ac9784;outline:none;"></textarea>
                  </div>

                  <p v-if="cOk" class="alert alert-ok">Tu mensaje fue enviado. ¡Te responderemos pronto!</p>
                  <p v-if="cErr" class="alert alert-error">{{ cErr }}</p>

                  <div class="mt-5">
                    <button type="submit" class="btn-1" :disabled="cLoading">
                      {{ cLoading ? 'Enviando…' : 'Enviar' }}
                    </button>
                  </div>
                </div>
              </div>
            </form>
          </div>

          <!-- Mapa -->
          <div class="col-md-6">
            <div class="map_container">
              <div class="map-responsive">
                <iframe
                  width="600"
                  height="300"
                  frameborder="0"
                  style="border:0; width: 100%; height:100%"
                  allowfullscreen
                  src="https://www.google.com/maps/embed/v1/place?key=AIzaSyA0s1a7phLN0iaD6-UE7m4qP-z21pH0eSc&q=Loja%2C+Ecuador&language=es">
                </iframe>
              </div>
            </div>
          </div>
          <!-- /Mapa -->
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getEjerciciosHome } from '../services/ejercicios'
import { enviarContacto } from '@/services/contacto'

const items = ref([])
const loading = ref(true)
const error = ref(false)

const cNombre = ref('')
const cCorreo = ref('')
const cTelefono = ref('')
const cMensaje = ref('')

const cOk = ref(false)
const cErr = ref('')
const cLoading = ref(false) // <-- antes faltaba

onMounted(async () => {
  try {
    items.value = await getEjerciciosHome()
  } catch (e) {
    error.value = true
  } finally {
    loading.value = false
  }
})

async function onEnviar() {
  cOk.value = false
  cErr.value = ''

  // validación mínima
  if (!cNombre.value || !cCorreo.value || !cTelefono.value || !cMensaje.value) {
    cErr.value = 'Completa todos los campos'
    return
  }
  if (!/^\S+@\S+\.\S+$/.test(cCorreo.value)) {
    cErr.value = 'Correo inválido'
    return
  }
  if (!/^[\d\s+\-()]+$/.test(cTelefono.value)) {
    cErr.value = 'Teléfono inválido'
    return
  }

  cLoading.value = true
  try {
    await enviarContacto({
      nombre: cNombre.value,
      correo: cCorreo.value,
      telefono: cTelefono.value,
      mensaje: cMensaje.value
    })
    cOk.value = true
    cNombre.value = ''
    cCorreo.value = ''
    cTelefono.value = ''
    cMensaje.value = ''
  } catch (e) {
    cErr.value = e?.message || 'No se pudo enviar'
  } finally {
    cLoading.value = false
  }
}
</script>
