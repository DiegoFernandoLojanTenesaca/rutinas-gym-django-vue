<template>
  <section class="service_section layout_padding sub_page">
    <div class="container">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <div class="heading_container"><h2>Explorar ejercicios</h2></div>
      </div>

      <!-- Buscador -->
      <form @submit.prevent="onBuscar" class="auth_card mb-3" novalidate>
        <div class="form-field">
          <input v-model.trim="q" class="auth_input" type="text" placeholder="Buscar por nombre (ej. press, sentadilla…)" />
        </div>
        <div class="actions">
          <button class="btn-1" type="submit">Buscar</button>
        </div>
      </form>

      <!-- Estados -->
      <div v-if="loading" class="muted">Cargando…</div>
      <div v-else-if="error" class="text-danger">{{ error }}</div>

      <!-- Resultados -->
      <div v-else>
        <div v-if="paged.length" class="service_container exercises_grid">
          <div class="box exercise-card" v-for="it in paged" :key="it.id">
            <div class="thumb-wrap">
              <img class="thumb" :src="it.imagen || '/assets/images/s-1.jpg'" :alt="it.nombre" loading="lazy">
            </div>
            <h6 class="visible_heading mt-2 mb-1 text-center">{{ it.nombre }}</h6>
            <div class="text-center small muted">{{ it.categoria }} • {{ it.tiempo }}</div>
            <div class="link_box d-flex justify-content-center align-items-center">
              <RouterLink :to="`/ejercicio/${it.slug}`" title="Ver detalle"><img src="/assets/images/link.png" alt="Ver"></RouterLink>
            </div>
          </div>
        </div>

        <div v-else class="muted">Sin resultados.</div>

        <!-- Paginación -->
        <div v-if="totalPages > 1" class="d-flex justify-content-center align-items-center mt-3 gap-2">
          <button class="btn-1" @click="prev" :disabled="page===1">« Anterior</button>
          <span class="mx-2 muted small">Página {{ page }} de {{ totalPages }}</span>
          <button class="btn-1" @click="next" :disabled="page===totalPages">Siguiente »</button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { listEjercicios } from '@/services/ejercicios'

const q = ref('')
const all = ref([])

const loading = ref(true)
const error = ref('')

// paginación simple en cliente
const page = ref(1)
const pageSize = 12
const totalPages = computed(() => Math.max(1, Math.ceil(all.value.length / pageSize)))
const paged = computed(() => {
  const start = (page.value - 1) * pageSize
  return all.value.slice(start, start + pageSize)
})

function resetPage() { page.value = 1 }
function prev() { if (page.value > 1) page.value-- }
function next() { if (page.value < totalPages.value) page.value++ }

async function load(search = '') {
  loading.value = true; error.value = ''
  try {
    all.value = await listEjercicios(search)
    resetPage()
  } catch (e) {
    error.value = e?.message || 'No se pudo cargar'
  } finally {
    loading.value = false
  }
}

function onBuscar() {
  load(q.value)
}

onMounted(() => load())
</script>
