<template>
  <div :class="['hero_area', isHome ? '' : 'sub_page']">
    <!-- header -->
    <header class="header_section">
      <div class="container">
        <nav class="navbar navbar-expand-lg custom_nav-container">
          <RouterLink class="navbar-brand" to="/">
            <img src="/assets/images/logo.png" alt="" />
            <span>Lion GYM</span>
          </RouterLink>

            <div class="contact_nav">
              <ul class="navbar-nav">
                <li class="nav-item">
                  <RouterLink class="nav-link" to="/contact" title="Ver ubicación y contacto">
                    <img src="/assets/images/location.png" alt="Ubicación" />
                    <span>Ubicación</span>
                  </RouterLink>
                </li>
                <li class="nav-item">
                  <a class="nav-link" href="tel:+593939327368" title="Llamar">
                    <img src="/assets/images/call.png" alt="Teléfono" />
                    <span>Contacto: +593 939327368</span>
                  </a>
                </li>
                <li class="nav-item">
                  <a class="nav-link" href="mailto:lionGym_EC@gmail.com" title="Escribir correo">
                    <img src="/assets/images/envelope.png" alt="Correo" />
                    <span>lionGym_EC@gmail.com</span>
                  </a>
                </li>
              </ul>
            </div>

        </nav>
      </div>
    </header>
    <!-- /header -->

    <!-- navbar + (slider solo en Home) -->
    <section class="slider_section position-relative">
      <div class="container-fluid px-0">
        <div class="custom_nav2">
          <nav class="navbar navbar-expand-lg custom_nav-container">
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent">
              <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse show" id="navbarSupportedContent">
              <div class="d-flex flex-column flex-lg-row align-items-center">
                <ul class="navbar-nav">
                  <li class="nav-item" :class="{ active: isHome }">
                    <RouterLink class="nav-link" to="/">Inicio</RouterLink>
                  </li>
                  <li class="nav-item" :class="{ active: route.name === 'about' }">
                    <RouterLink class="nav-link" to="/about">Acerca de</RouterLink>
                  </li>
                  <li class="nav-item" :class="{ active: route.name === 'contact' }">
                    <RouterLink class="nav-link" to="/contact">Contáctenos</RouterLink>
                  </li>
                  <li class="nav-item" :class="{ active: route.name === 'explorar' }">
                    <RouterLink class="nav-link" to="/explorar">Explorar</RouterLink>
                  </li>
                  <li class="nav-item" :class="{ active: route.name === 'categorias' || route.name === 'categoria' }">
                    <RouterLink class="nav-link" to="/categorias">Categorías</RouterLink>
                  </li>
                   <!-- Auth: si no está logueado, mostrar Login -->
                  <li class="nav-item" v-if="!auth.isLogged" :class="{ active: route.name === 'login' }">
                    <RouterLink class="nav-link" to="/login">Iniciar Sesión</RouterLink>
                  </li>
                  <!-- Auth: si está logueado, saludo + salir -->
                  <li class="nav-item" v-else :class="{ active: route.name === 'perfil' }">
                    <RouterLink class="nav-link user-pill" to="/perfil">
                      Bienvenido, {{ auth.user?.nombre }}
                    </RouterLink>
                  </li>
                  <li class="nav-item" :class="{ active: route.name === 'panel' }" v-if="auth.isLogged">
                    <RouterLink class="nav-link" to="/panel">Mi Panel</RouterLink>
                  </li>
                  <li class="nav-item" v-if="auth.isLogged">
                    <a class="nav-link" href="#" @click.prevent="doLogout">Salir</a>
                  </li>
                </ul>

              </div>
            </div>
          </nav>
        </div>
      </div>

      <!-- SLIDER AQUÍ, SOLO EN HOME -->
      <div v-if="isHome" class="slider_container">
        <div id="carouselExampleIndicators" class="carousel slide" data-ride="carousel">
          <!-- tus indicadores/inner tal cual -->
          <div class="carousel-inner">
            <div class="carousel-item active">
              <div class="container">
                <div class="row">
                  <div class="col-lg-6 col-md-7 offset-md-6 offset-md-5">
                    <div class="detail-box">
                      <h2>Entrena mejor, más fácil</h2>
                      <h1>Rutinas para ti</h1>
                      <p> Lion GYM te ayuda a descubrir, crear y organizar rutinas de gimnasio. Encuentra ejercicios por categoría, guarda tus favoritos y lleva el control de tu progreso.</p>
                      <div class="btn-box">
                        <RouterLink to="/explorar" class="btn-1">Explorar rutinas</RouterLink>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div> <!-- /carousel-inner -->
        </div>
      </div>
      <!-- /SLIDER -->
    </section>
  </div>

  <!-- contenido de cada ruta -->
  <RouterView />

  <!-- info + footer (global) -->
  <section class="info_section layout_padding2-top">
    <div class="container">
      <div class="info_form">
        <h4>¿Quieres recibir nuestras novedades?</h4>
        <form @submit.prevent>
          <input type="email" placeholder="Ingresa tu correo" />
          <div class="d-flex justify-content-end">
            <button type="submit">Suscribirme</button>
          </div>
        </form>
      </div>
    </div>

    <div class="container">
      <div class="row">
        <div class="col-md-3">
          <h6>Acerca de Lion GYM</h6>
          <p>Somos una plataforma para descubrir y gestionar rutinas de gimnasio. Explora ejercicios por categorías, organiza tus entrenamientos y mejora cada día.</p>
        </div>

        <div class="col-md-2 offset-md-1">
          <h6>Menú</h6>
            <ul>
              <li :class="{ active: isHome }"><RouterLink to="/">Inicio</RouterLink></li>
              <li :class="{ active: route.name === 'about' }"><RouterLink to="/about">Acerca de</RouterLink></li>
              <li :class="{ active: route.name === 'categorias' || route.name === 'categoria' }"><RouterLink to="/categorias">Categorías</RouterLink></li>
              <li :class="{ active: route.name === 'explorar' }"><RouterLink to="/explorar">Explorar</RouterLink></li>
              <li :class="{ active: route.name === 'contact' }"><RouterLink to="/contact">Contáctenos</RouterLink></li>
              <li v-if="!auth.isLogged" :class="{ active: route.name === 'login' }">
                <RouterLink to="/login">Iniciar Sesión</RouterLink>
              </li>
              <li v-else :class="{ active: route.name === 'panel' }">
                <RouterLink to="/panel">Mi Panel</RouterLink>
              </li>
            </ul>
        </div>

        <div class="col-md-3">
          <h6>Enlaces útiles</h6>
            <ul>
              <li><a href="#">Preguntas frecuentes</a></li>
              <li><a href="#">Guía de inicio</a></li>
              <li><a href="#">Soporte</a></li>
              <li><a href="#">Términos y condiciones</a></li>
              <li><a href="#">Política de privacidad</a></li>
            </ul>
        </div>

        <div class="col-md-3">
          <h6>Contáctanos</h6>
          <div class="info_link-box">
            <RouterLink to="/contact">
              <img src="/assets/images/location-white.png" alt="Ubicación" />
              <span>Loja, Ecuador</span>
            </RouterLink>
            <a href="tel:+593939327368">
              <img src="/assets/images/call-white.png" alt="Teléfono" />
              <span>+593 939327368</span>
            </a>
            <a href="mailto:lionGym_EC@gmail.com">
              <img src="/assets/images/mail-white.png" alt="Correo" />
              <span>lionGym_EC@gmail.com</span>
            </a>
          </div>
          <div class="info_social">
            <div><a href=""><img src="/assets/images/facebook-logo-button.png" alt="" /></a></div>
            <div><a href=""><img src="/assets/images/twitter-logo-button.png" alt="" /></a></div>
            <div><a href=""><img src="/assets/images/linkedin.png" alt="" /></a></div>
            <div><a href=""><img src="/assets/images/instagram.png" alt="" /></a></div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="container-fluid footer_section">
    <p>© {{ year }} Todos los derechos reservados</p>
  </section>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const route = useRoute();
const router = useRouter();
const auth = useAuthStore();

const isHome = computed(() => route.name === 'home');
const year = new Date().getFullYear();

function doLogout() {
  auth.logout();
  router.push('/');
}
</script>
