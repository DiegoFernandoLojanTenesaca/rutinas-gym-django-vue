<template>
  <section class="service_section layout_padding sub_page">
    <div class="container">
      <div class="d-flex justify-content-between align-items-center mb-2">
        <div class="heading_container"><h2>{{ titulo }}</h2></div>
        <RouterLink class="btn-1" to="/categorias">← Categorías</RouterLink>
      </div>

      <!-- Buscador dentro de la categoría -->
      <form @submit.prevent="onBuscar" class="auth_card mb-3" novalidate>
        <div class="form-field">
          <input v-model.trim="q" class="auth_input" type="text" placeholder="Filtrar por nombre (opcional)" />
        </div>
        <div class="actions">
          <button class="btn-1" type="submit">Buscar</button>
        </div>
      </form>

      <div v-if="loading" class="muted">Cargando…</div>
      <div v-else-if="error" class="text-danger">{{ error }}</div>

      <div v-else>
        <div v-if="items.length" class="service_container exercises_grid">
          <div class="box exercise-card" v-for="it in items" :key="it.id">
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
        <div v-else class="muted">Sin resultados en esta categoría.</div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { getCategorias } from '@/services/categorias'
import { httpGet } from '@/services/http'

const route = useRoute()
const id = computed(() => route.params.id)

const categorias = ref([])
const cat = computed(() => categorias.value.find(c => String(c.id) === String(id.value)) || null)
const titulo = computed(() => cat.value ? `Categoría: ${cat.value.nombre}` : 'Categoría')

const q = ref('')
const items = ref([])
const loading = ref(true)
const error = ref('')

async function load() {
  loading.value = true; error.value = ''
  try {
    // aseguramos tener categorías para mostrar el título
    if (!categorias.value.length) categorias.value = await getCategorias()

    const params = new URLSearchParams({ categoria_id: id.value, search: q.value || '' }).toString()
    const body = await httpGet(`ejercicios-buscador?${params}`)
    items.value = body.data || []
  } catch (e) {
    error.value = e?.message || 'No se pudo cargar'
  } finally {
    loading.value = false
  }
}

function onBuscar() {
  load()
}

onMounted(load)
// recarga si cambia :id desde navegación interna
watch(id, load)
</script>
