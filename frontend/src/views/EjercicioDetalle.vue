<template>
  <section class="service_section layout_padding">
    <div class="container">
      <div class="heading_container"><h2>{{ loading ? 'Cargando…' : ejercicio?.nombre }}</h2></div>

      <div v-if="error" class="text-danger">No se pudo cargar el ejercicio.</div>

      <div v-else-if="ejercicio" class="row">
        <div class="col-12 col-lg-6 mb-4">
          <div class="thumb-wrap"><img class="thumb" :src="ejercicio.imagen" :alt="ejercicio.nombre"></div>
        </div>
        <div class="col-12 col-lg-6">
          <h5 class="mb-2">{{ ejercicio.categoria }}</h5>
          <p class="mb-3"><strong>Series/Tiempo:</strong> {{ ejercicio.tiempo }}</p>
          <p class="mb-4">{{ ejercicio.descripcion }}</p>
          <RouterLink to="/" class="btn-1">← Volver</RouterLink>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { getEjercicioPorSlug } from '../services/ejercicios'
const props = defineProps({ slug: { type: String, required: true } })

const ejercicio = ref(null)
const loading = ref(true)
const error = ref(false)

onMounted(async () => {
  try {
    ejercicio.value = await getEjercicioPorSlug(props.slug)
  } catch (e) {
    error.value = true
  } finally {
    loading.value = false
  }
})
</script>
