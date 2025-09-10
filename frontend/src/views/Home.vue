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
      <div class="heading_container"><h2>Why Choose Us</h2></div>
      <div class="us_container">
        <div class="box"><div class="img-box"><img src="/assets/images/u-1.png" alt=""></div><div class="detail-box"><h5>QUALITY EQUIPMENT</h5><p>ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor</p></div></div>
        <div class="box"><div class="img-box"><img src="/assets/images/u-2.png" alt=""></div><div class="detail-box"><h5>HEALTHY NUTRITION PLAN</h5><p>ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor</p></div></div>
        <div class="box"><div class="img-box"><img src="/assets/images/u-3.png" alt=""></div><div class="detail-box"><h5>SHOWER SERVICE</h5><p>ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor</p></div></div>
        <div class="box"><div class="img-box"><img src="/assets/images/u-4.png" alt=""></div><div class="detail-box"><h5>UNIQUE TO YOUR NEEDS</h5><p>ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor</p></div></div>
      </div>
    </div>
  </section>

  <!-- CONTACT BLOCK (home) -->
  <section class="contact_section layout_padding" id="contactSection">
    <div class="container">
      <div class="heading_container"><h2><span>Get In Touch</span></h2></div>
      <div class="layout_padding2-top">
        <div class="row">
          <div class="col-md-6 ">
            <form action="">
              <div class="contact_form-container">
                <div>
                  <div><input type="text" placeholder="Name" /></div>
                  <div><input type="email" placeholder="Email" /></div>
                  <div><input type="text" placeholder="Phone Number" /></div>
                  <div class="mt-5"><input type="text" placeholder="Message" /></div>
                  <div class="mt-5"><button type="submit">Send</button></div>
                </div>
              </div>
            </form>
          </div>
          <div class="col-md-6">
            <div class="map_container">
              <div class="map-responsive">
                <iframe
                  src="https://www.google.com/maps/embed/v1/place?key=AIzaSyA0s1a7phLN0iaD6-UE7m4qP-z21pH0eSc&q=Eiffel+Tower+Paris+France"
                  width="600" height="300" frameborder="0"
                  style="border:0; width: 100%; height:100%" allowfullscreen
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getEjerciciosHome } from '../services/ejercicios'

const items = ref([])
const loading = ref(true)
const error = ref(false)

onMounted(async () => {
  try {
    items.value = await getEjerciciosHome()
  } catch (e) {
    error.value = true
  } finally {
    loading.value = false
  }
})
</script>
