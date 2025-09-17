import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';
import { setOnUnauthorized } from '@/services/http';

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router);

// Restaurar sesión antes de montar
import { useAuthStore } from '@/stores/auth';
const auth = useAuthStore();
auth.restoreFromStorage();

setOnUnauthorized(() => {
  // cierra sesión y redirige a login con motivo
  auth.logout();
  router.push({ name: 'login', query: { reason: 'expired' } });
});

app.mount('#app');
