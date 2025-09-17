<template>
  <section class="service_section layout_padding sub_page">
    <div class="container">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <div class="heading_container"><h2>Mis ejercicios</h2></div>
        <RouterLink class="btn-1" :to="{ name: 'ejercicio-nuevo' }">+ Nuevo</RouterLink>
      </div>

            <!-- Filtros / Orden -->
      <div class="auth_card filters_bar">
        <div class="row">
          <div class="col">
            <select class="auth_input" v-model="filtros.categoriaId">
              <option value="">Todas las categorías</option>
              <option v-for="c in categorias" :key="c.id" :value="String(c.id)">{{ c.nombre }}</option>
            </select>
          </div>
          <div class="col">
            <input class="auth_input" v-model.trim="filtros.search" type="text" placeholder="Buscar por nombre…" />
          </div>
          <div class="col">
            <select class="auth_input" v-model="filtros.order">
              <option value="recientes">Recientes primero</option>
              <option value="antiguos">Antiguos primero</option>
              <option value="az">Nombre A-Z</option>
              <option value="za">Nombre Z-A</option>
            </select>
          </div>
        </div>
      </div>

      <div v-if="loading" class="text-muted">Cargando…</div>
      <div v-else-if="error" class="text-danger">{{ error }}</div>

      <div v-else>
        <!-- Si hay resultados -->
        <template v-if="filteredTotal > 0">
          <div class="service_container exercises_grid">
            <div class="box exercise-card" v-for="it in pageItems" :key="it.id">
              <div class="thumb-wrap">
                <img class="thumb" :src="it.imagen || '/assets/images/s-1.jpg'" :alt="it.nombre" loading="lazy">
              </div>
              <h6 class="visible_heading mt-2 mb-1 text-center">{{ it.nombre }}</h6>
              <div class="text-center small muted">{{ it.categoria }} • {{ it.tiempo }}</div>

              <div class="mt-2 d-flex justify-content-center gap-2">
                <RouterLink class="btn-1" :to="{ name: 'ejercicio-editar', params: { id: it.id } }">Editar</RouterLink>
                <button class="btn-1" @click="onDelete(it)" :disabled="loadingDel === it.id">
                  {{ loadingDel === it.id ? 'Eliminando…' : 'Eliminar' }}
                </button>
              </div>
            </div>
          </div>

          <!-- Paginación -->
          <div v-if="totalPages > 1" class="d-flex justify-content-center align-items-center mt-3 gap-2">
            <button class="btn-1" @click="prevPage" :disabled="page===1">« Anterior</button>
            <span class="mx-2 muted small">Página {{ page }} de {{ totalPages }}</span>
            <button class="btn-1" @click="nextPage" :disabled="page===totalPages">Siguiente »</button>
          </div>
        </template>

        <!-- Sin resultados tras filtro -->
        <div v-else class="muted">No hay ejercicios que coincidan con el filtro.</div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { listByUser, deleteEjercicio } from '@/services/ejerciciosPanel';
import { getCategorias } from '@/services/categorias';

const auth = useAuthStore();

// Dataset completo (del backend)
const all = ref([]);

// Catálogo de categorías para filtros
const categorias = ref([]);

// Estado de filtros y orden
const filtros = ref({
  categoriaId: '',     // string o ''
  search: '',          // texto
  order: 'recientes',  // 'recientes' | 'antiguos' | 'az' | 'za'
});

// Paginación
const page = ref(1);
const perPage = ref(8);

// Loading/errores
const loading = ref(true);
const error = ref('');
const loadingDel = ref(null);

// 1) Filtrado
const filtered = computed(() => {
  let arr = all.value;

  // por categoría
  if (filtros.value.categoriaId) {
    const cid = String(filtros.value.categoriaId);
    arr = arr.filter(it => String(it.categoria_id) === cid);
  }

  // por texto en nombre
  if (filtros.value.search) {
    const q = filtros.value.search.toLowerCase();
    arr = arr.filter(it => (it.nombre || '').toLowerCase().includes(q));
  }

  // 2) Orden
  if (filtros.value.order === 'recientes') {
    arr = [...arr].sort((a, b) => b.id - a.id);
  } else if (filtros.value.order === 'antiguos') {
    arr = [...arr].sort((a, b) => a.id - b.id);
  } else if (filtros.value.order === 'az') {
    arr = [...arr].sort((a, b) => (a.nombre || '').localeCompare(b.nombre || ''));
  } else if (filtros.value.order === 'za') {
    arr = [...arr].sort((a, b) => (b.nombre || '').localeCompare(a.nombre || ''));
  }

  return arr;
});

const filteredTotal = computed(() => filtered.value.length);

// 3) Slice paginado (después de filtrar/ordenar)
const totalPages = computed(() => Math.max(1, Math.ceil(filteredTotal.value / perPage.value)));
const pageItems = computed(() => {
  const start = (page.value - 1) * perPage.value;
  return filtered.value.slice(start, start + perPage.value);
});

function nextPage() { if (page.value < totalPages.value) page.value++; }
function prevPage() { if (page.value > 1) page.value--; }

// Si cambias filtros, vuelve a la página 1
watch(filtros, () => { page.value = 1; }, { deep: true });

async function load() {
  loading.value = true; error.value = '';
  try {
    // catálogos y datos del usuario
    categorias.value = await getCategorias();
    all.value = await listByUser(auth.user.id);
    if (page.value > totalPages.value) page.value = totalPages.value;
  } catch (e) {
    error.value = e?.message || 'No se pudo cargar';
  } finally {
    loading.value = false;
  }
}

async function onDelete(it) {
  if (!confirm(`¿Eliminar "${it.nombre}"?`)) return;
  loadingDel.value = it.id;
  try {
    await deleteEjercicio(it.id);
    await load();
  } catch (e) {
    alert(e?.message || 'No se pudo eliminar');
  } finally {
    loadingDel.value = null;
  }
}

onMounted(load);
</script>
