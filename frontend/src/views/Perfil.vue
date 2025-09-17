<template>
  <section class="service_section layout_padding sub_page">
    <div class="container">
      <div class="heading_container"><h2>Mi perfil</h2></div>

      <div class="auth_card" style="max-width:720px">
        <!-- Datos básicos -->
        <h5 class="mb-2">Datos básicos</h5>
        <form @submit.prevent="onGuardarPerfil">
          <div class="form-field">
            <label class="sr-only" for="p-nombre">Nombre</label>
            <input id="p-nombre" v-model.trim="form.nombre" type="text" class="auth_input" required placeholder="Nombre" :disabled="loadingPerfil" />
          </div>
          <div class="form-field">
            <label class="sr-only" for="p-correo">Correo</label>
            <input
              id="p-correo"
              v-model.trim="form.correo"
              type="email"
              class="auth_input is-readonly"
              required
              placeholder="Correo"
              disabled
              readonly
              aria-disabled="true"
              title="El correo no se puede modificar"
            />
          </div>

          <p v-if="okPerfil" class="alert alert-ok">Perfil actualizado.</p>
          <p v-if="errPerfil" class="alert alert-error">{{ errPerfil }}</p>

          <div class="actions">
            <button class="btn-1" type="submit" :disabled="loadingPerfil">
              {{ loadingPerfil ? 'Guardando…' : 'Guardar cambios' }}
            </button>
          </div>
        </form>

        <hr class="my-4">

        <!-- Cambiar contraseña -->
        <h5 class="mb-2">Cambiar contraseña</h5>
        <form @submit.prevent="onCambiarPass">
          <div class="form-field has-append">
            <label class="sr-only" for="p-actual">Contraseña actual</label>
            <input id="p-actual" :type="showA ? 'text':'password'" v-model.trim="pass.actual" class="auth_input" required placeholder="Contraseña actual" :disabled="loadingPass" />
            <button type="button" class="append-btn icon" @click="showA=!showA" :disabled="loadingPass" title="Mostrar/Ocultar">
              <svg v-if="showA" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8Z"/><circle cx="12" cy="12" r="3"/></svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17.94 17.94A10.94 10.94 0 0 1 12 20C5 20 1 12 1 12a21.77 21.77 0 0 1 5.06-6.94"/><path d="M10.58 10.58a3 3 0 0 0 4.24 4.24"/><path d="M23 1 1 23"/></svg>
            </button>
          </div>

          <div class="form-field has-append">
            <label class="sr-only" for="p-nueva">Nueva contraseña</label>
            <input id="p-nueva" :type="showN ? 'text':'password'" v-model.trim="pass.nueva" minlength="6" class="auth_input" required placeholder="Nueva contraseña (mín. 6)" :disabled="loadingPass" />
            <button type="button" class="append-btn icon" @click="showN=!showN" :disabled="loadingPass" title="Mostrar/Ocultar">
              <svg v-if="showN" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8Z"/><circle cx="12" cy="12" r="3"/></svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17.94 17.94A10.94 10.94 0 0 1 12 20C5 20 1 12 1 12a21.77 21.77 0 0 1 5.06-6.94"/><path d="M10.58 10.58a3 3 0 0 0 4.24 4.24"/><path d="M23 1 1 23"/></svg>
            </button>
          </div>

          <div class="form-field">
            <label class="sr-only" for="p-rep">Repetir nueva contraseña</label>
            <input id="p-rep" :type="showN ? 'text':'password'" v-model.trim="pass.rep" minlength="6" class="auth_input" required placeholder="Repetir nueva contraseña" :disabled="loadingPass" />
          </div>

          <p v-if="okPass" class="alert alert-ok">Contraseña actualizada.</p>
          <p v-if="errPass" class="alert alert-error">{{ errPass }}</p>

          <div class="actions">
            <button class="btn-1" type="submit" :disabled="loadingPass">
              {{ loadingPass ? 'Actualizando…' : 'Cambiar contraseña' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { getPerfil, updatePerfil, cambiarPassword } from '@/services/perfil';

const auth = useAuthStore();

// estado datos básicos
const form = ref({ nombre: '', correo: '' });
const loadingPerfil = ref(false);
const okPerfil = ref(false);
const errPerfil = ref('');

// estado contraseña
const pass = ref({ actual: '', nueva: '', rep: '' });
const loadingPass = ref(false);
const okPass = ref(false);
const errPass = ref('');
const showA = ref(false);
const showN = ref(false);

onMounted(async () => {
  try {
    loadingPerfil.value = true;
    const me = await getPerfil();
    form.value.nombre = me.nombre || auth.user?.nombre || '';
    form.value.correo = me.correo || '';
  } catch (e) {
    errPerfil.value = e?.message || 'No se pudo cargar el perfil';
  } finally {
    loadingPerfil.value = false;
  }
});

async function onGuardarPerfil() {
  okPerfil.value = false; errPerfil.value = ''; loadingPerfil.value = true;
  try {
    await updatePerfil({ nombre: form.value.nombre, correo: form.value.correo });
    okPerfil.value = true;
    // reflejar nombre nuevo en el header
    auth.updateLocalUser({ nombre: form.value.nombre });
  } catch (e) {
    errPerfil.value = e?.message || 'No se pudo guardar';
  } finally {
    loadingPerfil.value = false;
  }
}

async function onCambiarPass() {
  okPass.value = false; errPass.value = '';
  if (pass.value.nueva !== pass.value.rep) {
    errPass.value = 'Las contraseñas no coinciden';
    return;
  }
  loadingPass.value = true;
  try {
    await cambiarPassword({ actual: pass.value.actual, nueva: pass.value.nueva });
    okPass.value = true;
    pass.value = { actual:'', nueva:'', rep:'' };
  } catch (e) {
    errPass.value = e?.message || 'No se pudo actualizar la contraseña';
  } finally {
    loadingPass.value = false;
  }
}
</script>

<style scoped>
.my-4{ margin:16px 0; }
.mb-2{ margin-bottom:8px; }
</style>
