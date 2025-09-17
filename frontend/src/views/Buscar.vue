<template>
  <section class="service_section layout_padding sub_page">
    <div class="container">
      <div class="heading_container"><h2>Buscar ejercicios</h2></div>

      <div class="auth_card">
        <div class="form-field">
          <select class="auth_input" v-model="categoria_id" required>
            <option value="" disabled>Selecciona categoría</option>
            <option v-for="c in categorias" :key="c.id" :value="String(c.id)">{{ c.nombre }}</option>
          </select>
        </div>
        <div class="form-field">
          <input
            class="auth_input"
            v-model.trim="search"
            type="text"
            placeholder="Escribe para buscar…"
            :disabled="!categoria_id || loading"
          />
        </div>
        <p class="small muted" v-if="!categoria_id">Selecciona una categoría para activar la búsqueda.</p>
      </div>

      <div class="mt-2" v-if="loading">Buscando…</div>
      <div class="mt-2 text-danger" v-else-if="error">{{ error }}</div>

      <div v-else-if="items.length" class="service_container exercises_grid">
        <div class="box exercise-card" v-for="it in items" :key="it.id">
          <div class="thumb-wrap">
            <img class="thumb" :src="it.imagen || '/assets/images/s-1.jpg'" :alt="it.nombre" loading="lazy">
          </div>
          <h6 class="visible_heading mt-2 mb-1 text-center">{{ it.nombre }}</h6>
          <div class="link_box d-flex justify-content-center align-items-center">
            <RouterLink :to="`/ejercicio/${it.slug}`"><img src="/assets/images/link.png" alt="Ver"></RouterLink>
          </div>
        </div>
      </div>

      <div class="muted" v-else-if="accion">Sin resultados.</div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { getCategorias } from '@/services/categorias';
import { buscarEjercicios } from '@/services/buscador';

const categorias = ref([]);
const categoria_id = ref('');
const search = ref('');
const items = ref([]);
const loading = ref(false);
const error = ref('');
const accion = ref(false); // indica que ya hicimos al menos una búsqueda

let timer = null;

onMounted(async () => {
  categorias.value = await getCategorias();
});

// Cuando cambie la categoría, re-lanza la búsqueda (con debounce mínimo)
watch(categoria_id, () => {
  items.value = [];
  accion.value = false;
  if (!categoria_id.value) return;
  doSearch();
});

// Búsqueda en vivo (cada vez que escribe, con debounce 300ms)
watch(search, () => {
  if (!categoria_id.value) return;
  clearTimeout(timer);
  timer = setTimeout(doSearch, 300);
});

async function doSearch() {
  error.value = '';
  loading.value = true;
  accion.value = true;
  try {
    items.value = await buscarEjercicios({
      categoria_id: categoria_id.value,
      search: search.value || ''
    });
  } catch (e) {
    error.value = e?.message || 'No se pudo buscar';
    items.value = [];
  } finally {
    loading.value = false;
  }
}
</script>
