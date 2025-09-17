<template>
  <!-- EJERCICIOS (desde backend) -->
  <section class="service_section layout_padding">
    <div class="container">
      <div class="heading_container"><h2>Ejercicios destacados</h2></div>

      <div v-if="loading" class="text-muted">Cargando ejercicios…</div>
      <div v-else-if="error" class="text-danger">No se pudieron cargar los ejercicios.</div>

      <div class="service_container exercises_grid" v-else-if="items.length">
        <div class="box exercise-card" v-for="it in items" :key="it.id">
          <div class="thumb-wrap">
            <img class="thumb" :src="it.imagen || '/assets/images/s-1.jpg'" :alt="it.nombre">
          </div>

          <h6 class="visible_heading mt-2 mb-1 text-center">{{ it.nombre }}</h6>

            <div class="link_box d-flex justify-content-center align-items-center">
            <RouterLink :to="`/ejercicio/${it.slug}`" title="Ver detalle" aria-label="Ver detalle">
              <img src="/assets/images/link.png" alt="Ver">
            </RouterLink>
          </div>
        </div>
      </div>

      <div v-else class="text-muted">No hay ejercicios para mostrar.</div>
    </div>
  </section>

<!-- WHY US -->
<section class="us_section layout_padding">
  <div class="container">
    <div class="heading_container"><h2>¿Por qué elegir Lion GYM?</h2></div>

    <div class="us_container">
      <div class="box">
        <div class="img-box">
          <img src="/assets/images/u-1.png" alt="Ejercicios verificados">
        </div>
        <div class="detail-box">
          <h5>EJERCICIOS VERIFICADOS</h5>
          <p>
            Catálogo por grupos musculares con imágenes y descripciones claras.
            Encuentra lo que necesitas en segundos.
          </p>
        </div>
      </div>

      <div class="box">
        <div class="img-box">
          <img src="/assets/images/u-2.png" alt="Planifica tu entrenamiento">
        </div>
        <div class="detail-box">
          <h5>PLANIFICA TU ENTRENAMIENTO</h5>
          <p>
            Crea, edita y organiza tus rutinas con series, repeticiones y tiempos.
            Todo en un solo lugar.
          </p>
        </div>
      </div>

      <div class="box">
        <div class="img-box">
          <img src="/assets/images/u-3.png" alt="Simple y rápido">
        </div>
        <div class="detail-box">
          <h5>SIMPLE Y RÁPIDO</h5>
          <p>
            Interfaz limpia y veloz, pensada para móvil y escritorio.
            Sin distracciones para que te enfoques en entrenar.
          </p>
        </div>
      </div>

      <div class="box">
        <div class="img-box">
          <img src="/assets/images/u-4.png" alt="Hecho a tu medida">
        </div>
        <div class="detail-box">
          <h5>HECHO A TU MEDIDA</h5>
          <p>
            Filtra por categorías, guarda tus favoritos y vuelve a ellos cuando quieras.
            Tus rutinas, a tu estilo.
          </p>
        </div>
      </div>
    </div>
  </div>
</section>

</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getEjerciciosHome } from '../services/ejercicios'
import { enviarContacto } from '@/services/contacto';

const items = ref([])
const loading = ref(true)
const error = ref(false)
const cNombre = ref('');
const cCorreo = ref('');
const cTelefono = ref('');
const cMensaje = ref('');
const cOk = ref(false);
const cErr = ref('');


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
  cOk.value = false; cErr.value = '';
  // validación mínima
  if (!cNombre.value || !cCorreo.value || !cTelefono.value || !cMensaje.value) {
    cErr.value = 'Completa todos los campos';
    return;
  }
  if (!/^\S+@\S+\.\S+$/.test(cCorreo.value)) {
    cErr.value = 'Correo inválido';
    return;
  }
  if (!/^[\d\s+\-()]+$/.test(cTelefono.value)) {
    cErr.value = 'Teléfono inválido';
    return;
  }

  cLoading.value = true;
  try {
    await enviarContacto({
      nombre: cNombre.value,
      correo: cCorreo.value,
      telefono: cTelefono.value,
      mensaje: cMensaje.value
    });
    cOk.value = true;
    cNombre.value = cCorreo.value = cTelefono.value = cMensaje.value = '';
  } catch (e) {
    cErr.value = e?.message || 'No se pudo enviar';
  } finally {
    cLoading.value = false;
  }
}



</script>
