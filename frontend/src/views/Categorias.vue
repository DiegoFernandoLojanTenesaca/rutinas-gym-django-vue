<template>
  <section class="service_section layout_padding sub_page">
    <div class="container">
      <div class="heading_container"><h2>Categorías</h2></div>

      <div v-if="loading" class="muted">Cargando…</div>
      <div v-else-if="error" class="text-danger">{{ error }}</div>

      <div v-else>
        <div v-if="items.length" class="service_container exercises_grid">
          <RouterLink
            v-for="c in items"
            :key="c.id"
            class="box exercise-card cat-card-link"
            :to="{ name:'categoria', params:{ id: c.id } }"
            :title="`Ver ejercicios de ${c.nombre}`"
          >
            <div class="thumb-wrap cat-thumb">
              <!-- 1) Miniatura real si hay ejercicios -->
              <img
                v-if="c._thumb"
                class="thumb"
                :src="c._thumb"
                :alt="`Imagen aleatoria de ${c.nombre}`"
                loading="lazy"
              />
              <!-- 2) Placeholder si no hay -->
              <div v-else class="cat-placeholder">
                <span class="cat-inicial">{{ c.nombre?.[0] || '?' }}</span>
              </div>

              <!-- Insignia si está vacía -->
              <span v-if="c._count === 0" class="cat-badge-empty">Sin ejercicios</span>
            </div>

            <h6 class="visible_heading mt-2 mb-1 text-center">{{ c.nombre }}</h6>

            <!-- Icono centrado (opcional) -->
            <div class="link_box d-flex justify-content-center align-items-center">
              <img src="/assets/images/link.png" alt="Ver" />
            </div>
          </RouterLink>
        </div>

        <div v-else class="muted">Aún no hay categorías.</div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getCategorias } from '@/services/categorias'
import { httpGet } from '@/services/http'

const items = ref([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    loading.value = true
    // 1) Traer categorías
    const cats = await getCategorias()

    // 2) Para cada categoría, pedir sus ejercicios y elegir uno aleatorio como portada
    const withThumbs = await Promise.all(
      cats.map(async (c) => {
        try {
          const body = await httpGet(`ejercicios-buscador?categoria_id=${c.id}`)
          const data = Array.isArray(body?.data) ? body.data : []
          const count = data.length
          let thumb = null

          if (count > 0) {
            // Elegir uno al azar
            const rand = Math.floor(Math.random() * count)
            thumb = data[rand]?.imagen || null
          }

          return { ...c, _thumb: thumb, _count: count }
        } catch {
          // Si falló la carga de ejercicios, dejar sin miniatura
          return { ...c, _thumb: null, _count: 0 }
        }
      })
    )

    items.value = withThumbs
  } catch (e) {
    error.value = e?.message || 'No se pudo cargar'
  } finally {
    loading.value = false
  }
})
</script>
