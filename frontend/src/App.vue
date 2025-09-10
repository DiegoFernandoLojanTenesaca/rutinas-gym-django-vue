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
                <RouterLink class="nav-link" to="/services">
                  <img src="/assets/images/location.png" alt="" />
                  <span>Ubicación</span>
                </RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink class="nav-link" to="/services">
                  <img src="/assets/images/call.png" alt="" />
                  <span>Contacto : + 593 939327368</span>
                </RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink class="nav-link" to="/services">
                  <img src="/assets/images/envelope.png" alt="" />
                  <span>lionGym_EC@gmail.com</span>
                </RouterLink>
              </li>
            </ul>
          </div>
        </nav>
      </div>
    </header>
    <!-- /header -->

    <!-- navbar + (slider solo en Home) -->
    <section class="slider_section position-relative">
      <div class="container">
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

                  <!-- Auth: si no está logueado, mostrar Login -->
                  <li class="nav-item" v-if="!auth.isLogged" :class="{ active: route.name === 'login' }">
                    <RouterLink class="nav-link" to="/login">Iniciar Sesión</RouterLink>
                  </li>
                  <!-- Auth: si está logueado, saludo + salir -->
                  <li class="nav-item" v-else>
                    <a class="nav-link" href="#" @click.prevent>
                      Hola, {{ auth.user?.nombre }}
                    </a>
                  </li>
                  <li class="nav-item" v-if="auth.isLogged">
                    <a class="nav-link" href="#" @click.prevent="doLogout">Salir</a>
                  </li>
                </ul>

                <form class="form-inline my-2 my-lg-0 ml-0 ml-lg-4 mb-3 mb-lg-0">
                  <button class="btn my-2 my-sm-0 nav_search-btn" type="button"></button>
                </form>
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
                      <h2>Consigue Tu Cuerpo</h2>
                      <h1>Aquí Fitness</h1>
                      <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
                      <div class="btn-box">
                        <a href="#" class="btn-1">Leer Más</a>
                        <a href="#" class="btn-2">Solicitar Cotización</a>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="carousel-item">
              <div class="container">
                <div class="row">
                  <div class="col-lg-6 col-md-7 offset-md-6 offset-md-5">
                    <div class="detail-box">
                      <h2>Consigue Tu Cuerpo</h2>
                      <h1>Aquí Fitness</h1>
                      <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.</p>
                      <div class="btn-box">
                        <a href="#" class="btn-1">Leer Más</a>
                        <a href="#" class="btn-2">Solicitar Cotización</a>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="carousel-item">
              <div class="container">
                <div class="row">
                  <div class="col-lg-6 col-md-7 offset-md-6 offset-md-5">
                    <div class="detail-box">
                      <h2>Consigue Tu Cuerpo</h2>
                      <h1>Aquí Fitness</h1>
                      <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.</p>
                      <div class="btn-box">
                        <a href="#" class="btn-1">Leer Más</a>
                        <a href="#" class="btn-2">Solicitar Cotización</a>
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
        <h4>Our Newsletter</h4>
        <form action="">
          <input type="text" placeholder="Enter your email" />
          <div class="d-flex justify-content-end">
            <button>subscribe</button>
          </div>
        </form>
      </div>
    </div>

    <div class="container">
      <div class="row">
        <div class="col-md-3">
          <h6>Acerca de Lion GYM</h6>
          <p>consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation u</p>
        </div>

        <div class="col-md-2 offset-md-1">
          <h6>Menus</h6>
          <ul>
            <li :class="{ active: isHome }"><RouterLink to="/">Home</RouterLink></li>
            <li :class="{ active: route.name === 'about' }"><RouterLink to="/about">Acerca de</RouterLink></li>
            <li :class="{ active: route.name === 'services' }"><RouterLink to="/services">Servicios</RouterLink></li>
            <li :class="{ active: route.name === 'contact' }"><RouterLink to="/contact">Contáctenos</RouterLink></li>

            <!-- Auth en footer -->
            <li v-if="!auth.isLogged" :class="{ active: route.name === 'login' }">
              <RouterLink to="/login">Iniciar Sesión</RouterLink>
            </li>
            <li v-else>
              <a href="#" @click.prevent="doLogout">Cerrar sesión</a>
            </li>
          </ul>
        </div>

        <div class="col-md-3">
          <h6>Useful Links</h6>
          <ul>
            <li><a href="">Adipiscing</a></li>
            <li><a href="">Elit, sed</a></li>
            <li><a href="">do Eiusmod</a></li>
            <li><a href="">Tempor</a></li>
            <li><a href="">incididunt</a></li>
          </ul>
        </div>

        <div class="col-md-3">
          <h6>Contact Us</h6>
          <div class="info_link-box">
            <a href=""><img src="/assets/images/location-white.png" alt="" /><span>No.123, loram ipusm</span></a>
            <a href=""><img src="/assets/images/call-white.png" alt="" /><span>+01 12345678901</span></a>
            <a href=""><img src="/assets/images/mail-white.png" alt="" /><span>demo123@gmail.com</span></a>
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
    <p>© {{ year }} Todos los derechos reservados
      <a href="https://html.design/" target="_blank" rel="noopener">(diseño de Free Html Templates)</a>
    </p>
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
