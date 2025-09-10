<template>
  <section class="service_section layout_padding sub_page">
    <div class="container">
      <div class="auth_card">
        <div class="heading_container"><h2>Iniciar sesión</h2></div>

        <form @submit.prevent="onSubmit" novalidate>
          <!-- Correo -->
          <div class="form-field">
            <label for="login-email" class="sr-only">Correo</label>
            <input
              id="login-email"
              v-model.trim="correo"
              type="email"
              required
              autocomplete="email"
              placeholder="Correo"
              class="auth_input"
              :disabled="loading"
            />
          </div>

          <!-- Password -->
          <div class="form-field has-append">
            <label for="login-pass" class="sr-only">Contraseña</label>
            <input
              id="login-pass"
              v-model.trim="password"
              :type="showPassword ? 'text' : 'password'"
              required
              autocomplete="current-password"
              placeholder="Contraseña"
              class="auth_input"
              :disabled="loading"
            />
            <button
              type="button"
              class="append-btn icon"
              :aria-pressed="showPassword ? 'true' : 'false'"
              @click="showPassword = !showPassword"
              :disabled="loading"
              :title="showPassword ? 'Ocultar contraseña' : 'Mostrar contraseña'"
            >
              <!-- Ojo abierto -->
              <svg v-if="showPassword" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8Z"/>
                <circle cx="12" cy="12" r="3"/>
              </svg>
              <!-- Ojo cerrado -->
              <svg v-else xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <path d="M17.94 17.94A10.94 10.94 0 0 1 12 20C5 20 1 12 1 12a21.77 21.77 0 0 1 5.06-6.94"/>
                <path d="M10.58 10.58a3 3 0 0 0 4.24 4.24"/>
                <path d="M23 1 1 23"/>
              </svg>
            </button>
          </div>

          <!-- Mensajes -->
          <p v-if="error" class="alert alert-error" role="alert">{{ error }}</p>

          <!-- Acciones -->
          <div class="actions">
            <button type="submit" class="btn-1 w-100" :disabled="loading">
              {{ loading ? 'Ingresando…' : 'Ingresar' }}
            </button>
          </div>

          <p class="muted small mt-2">
            ¿No tienes cuenta?
            <RouterLink to="/register">Crear cuenta</RouterLink>
          </p>
        </form>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const correo = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')
const showPassword = ref(false)

async function onSubmit () {
  if (!correo.value || !password.value) {
    error.value = 'Completa tu correo y contraseña'
    return
  }
  error.value = ''
  loading.value = true
  try {
    await auth.login({ correo: correo.value, password: password.value })
    router.push('/') // vuelve a Home (o cambia por redirect si quieres)
  } catch (e) {
    // intenta leer mensaje del backend si viene
    error.value = e?.message || 'No se pudo iniciar sesión'
  } finally {
    loading.value = false
  }
}
</script>
