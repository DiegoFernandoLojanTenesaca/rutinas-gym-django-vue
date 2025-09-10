import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router);

// Restaurar sesión antes de montar
import { useAuthStore } from '@/stores/auth';
const auth = useAuthStore();
auth.restoreFromStorage();

app.mount('#app');
