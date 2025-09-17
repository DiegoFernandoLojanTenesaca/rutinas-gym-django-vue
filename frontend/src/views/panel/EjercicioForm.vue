<template>
  <section class="service_section layout_padding sub_page">
    <div class="container">
      <div class="heading_container">
        <h2>{{ isEdit ? 'Editar ejercicio' : 'Nuevo ejercicio' }}</h2>
      </div>

      <form @submit.prevent="onSubmit" class="auth_card">
        <div class="form-field">
          <input class="auth_input" v-model.trim="form.nombre" type="text" required placeholder="Nombre" />
        </div>

        <div class="form-field">
          <input class="auth_input" v-model.trim="form.tiempo" type="text" required placeholder="Series/Tiempo (ej. 4x12)" />
        </div>

        <div class="form-field">
          <select class="auth_input" v-model="form.categoria_id" required>
            <option value="" disabled>Selecciona categoría</option>
            <option v-for="c in categorias" :key="c.id" :value="c.id">{{ c.nombre }}</option>
          </select>
        </div>

        <div class="form-field">
          <textarea class="auth_input" v-model.trim="form.descripcion" required rows="4" placeholder="Descripción"></textarea>
        </div>

        <!-- Foto (requerida SOLO en crear) -->
        <div class="form-field" v-if="!isEdit">
          <input class="auth_input" type="file" accept="image/png,image/jpeg" @change="onPick" required />
          <div v-if="previewNueva" class="mt-2">
            <img :src="previewNueva" alt="preview" style="max-width:220px;border-radius:10px;margin-bottom:8px">
            <div>
              <button type="button" class="btn-1" @click="clearFile">Quitar imagen</button>
            </div>
          </div>
        </div>

        <!-- Cambiar foto (solo editar) -->
        <div class="form-field" v-else>
          <label class="small muted d-block mb-1">Foto actual</label>
          <img v-if="previewActual" :src="previewActual" alt="" style="max-width:220px;border-radius:10px;margin-bottom:8px">
          <div>
            <input class="auth_input" type="file" accept="image/png,image/jpeg" @change="onPick" />
            <button v-if="file" type="button" class="btn-1 mt-2" @click="onUploadFoto" :disabled="loadingFoto">
              {{ loadingFoto ? 'Subiendo…' : 'Actualizar foto' }}
            </button>
          </div>
        </div>

        <p v-if="msgOk" class="alert alert-ok">{{ msgOk }}</p>
        <p v-if="msgErr" class="alert alert-error">{{ msgErr }}</p>

        <div class="actions">
          <button class="btn-1" type="submit" :disabled="loading">
            {{ loading ? 'Guardando…' : (isEdit ? 'Guardar cambios' : 'Crear') }}
          </button>
          <RouterLink class="btn-1 ml-2" :to="{ name: 'panel' }">Cancelar</RouterLink>
        </div>
      </form>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { getCategorias } from '@/services/categorias';
import { createEjercicio, updateEjercicio, updateFoto } from '@/services/ejerciciosPanel';
import { httpGet } from '@/services/http';

const route = useRoute();
const router = useRouter();
const isEdit = computed(() => !!route.params.id);

const categorias = ref([]);
const form = ref({ nombre:'', tiempo:'', categoria_id:'', descripcion:'' });
const file = ref(null);

const loading = ref(false);
const loadingFoto = ref(false);
const msgOk = ref('');
const msgErr = ref('');
const previewActual = ref('');

const previewNueva = ref('');

// Cargar categorías y, si es edición, el ejercicio
onMounted(async () => {
  categorias.value = await getCategorias();
  if (isEdit.value) {
    const { data } = await httpGet(`ejercicios/${route.params.id}`); // reutilizamos endpoint por id
    form.value = {
      nombre: data.nombre,
      tiempo: data.tiempo,
      categoria_id: data.categoria_id,
      descripcion: data.descripcion,
    };
    previewActual.value = data.imagen || '';
  }
});

function onPick(e) {
  const f = e.target.files?.[0] || null;
  if (!f) { file.value = null; previewNueva.value = ''; return; }

  // Validaciones
  const okType = ['image/jpeg', 'image/png'].includes(f.type);
  const okSize = f.size <= 3 * 1024 * 1024; // 3MB
  if (!okType) {
    msgErr.value = 'La imagen debe ser JPEG o PNG';
    e.target.value = '';
    file.value = null;
    previewNueva.value = '';
    return;
  }
  if (!okSize) {
    msgErr.value = 'La imagen no debe superar 3 MB';
    e.target.value = '';
    file.value = null;
    previewNueva.value = '';
    return;
  }

  msgErr.value = '';
  file.value = f;

  // Preview: si estás CREANDO, muestra previewNueva; si EDITAS, se usará cuando “Actualizar foto”
  const reader = new FileReader();
  reader.onload = (ev) => {
    previewNueva.value = String(ev.target?.result || '');
  };
  reader.readAsDataURL(f);
}


async function onUploadFoto() {
  if (!file.value) return;
  loadingFoto.value = true; msgErr.value=''; msgOk.value='';
  try {
    await updateFoto(route.params.id, file.value);
    msgOk.value = 'Foto actualizada';
  } catch (e) {
    msgErr.value = e?.message || 'No se pudo actualizar la foto';
  } finally {
    loadingFoto.value = false;
  }
}

function clearFile() {
  file.value = null;
  previewNueva.value = '';
}

async function onSubmit() {
  msgErr.value=''; msgOk.value=''; loading.value = true;
  try {
    if (!isEdit.value) {
      if (!file.value) throw new Error('Adjunta una foto');
      await createEjercicio({ ...form.value, foto: file.value });
      msgOk.value = 'Ejercicio creado';
    } else {
      await updateEjercicio(route.params.id, form.value);
      msgOk.value = 'Cambios guardados';
    }
    setTimeout(() => router.push({ name: 'panel' }), 600);
  } catch (e) {
    msgErr.value = e?.message || 'No se pudo guardar';
  } finally {
    loading.value = false;
  }
}
</script>
