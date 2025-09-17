<template>
  <section class="about_section layout_padding sub_page about-hero">
    <div class="container">
      <div class="heading_container">
        <h2>Acerca de Lion GYM</h2>
      </div>

      <!-- Contenido alineado -->
      <div class="about-wrap">

        <!-- Texto + métricas + beneficios + CTAs -->
        <div class="detail-box">
          <p class="lead">
            En <strong>Lion GYM</strong> te ayudamos a construir rutinas efectivas sin complicarte.
            Explora ejercicios por categorías, guarda tus favoritos y organiza tus sesiones con
            series, repeticiones y tiempos. Todo queda en tu panel, siempre accesible y fácil de editar.
          </p>

          <!-- Métricas / confianza -->
          <div class="kpis">
            <div class="kpi">
              <h4>+100</h4>
              <span>Ejercicios listos</span>
            </div>
            <div class="kpi">
              <h4>24/7</h4>
              <span>Acceso a tu panel</span>
            </div>
            <div class="kpi">
              <h4>0 costo</h4>
              <span>Empezar es gratis</span>
            </div>
          </div>

          <!-- Beneficios cortos -->
          <ul class="bullets">
            <li>Catálogo visual por grupos musculares.</li>
            <li>Filtros rápidos y buscador por nombre.</li>
            <li>Creación y edición de rutinas en segundos.</li>
            <li>Seguridad con acceso de usuario y contraseña.</li>
          </ul>

          <!-- CTAs centradas -->
          <div class="ctas">
            <RouterLink class="btn-1" to="/explorar">Explorar ejercicios</RouterLink>
            <RouterLink class="btn-1" to="/categorias">Ver categorías</RouterLink>
            <RouterLink class="btn-1" to="/contact">Contáctanos</RouterLink>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
