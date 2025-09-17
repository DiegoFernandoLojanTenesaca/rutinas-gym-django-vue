import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth';

const Home = () => import('../views/Home.vue')
const About = () => import('../views/About.vue')
const Contact = () => import('../views/Contact.vue')
const EjercicioDetalle = () => import('../views/EjercicioDetalle.vue')
const Login = () => import('../views/Login.vue');
const Register = () => import('../views/Register.vue');
const Panel = () => import('../views/panel/Panel.vue');
const EjercicioForm = () => import('../views/panel/EjercicioForm.vue');
const Explorar = () => import('../views/Explorar.vue');
const Categorias = () => import('../views/Categorias.vue');
const CategoriaList = () => import('../views/CategoriaList.vue');
const Perfil = () => import('../views/Perfil.vue');

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'home', component: Home },
    { path: '/about', name: 'about', component: About },
    { path: '/contact', name: 'contact', component: Contact },
    { path: '/ejercicio/:slug', name: 'ejercicio-detalle', component: EjercicioDetalle, props: true },
    { path: '/login', name: 'login', component: Login },
    { path: '/register', name: 'register', component: Register },

    // Públicas
    { path: '/explorar', name: 'explorar', component: Explorar },
    { path: '/categorias', name: 'categorias', component: Categorias },
    { path: '/categoria/:id', name: 'categoria', component: CategoriaList, props: true },

    // Privadas (meta.requiresAuth)
    { path: '/panel', name: 'panel', component: Panel, meta: { requiresAuth: true } },
    { path: '/panel/ejercicios/nuevo', name: 'ejercicio-nuevo', component: EjercicioForm, meta: { requiresAuth: true } },
    { path: '/panel/ejercicios/:id/editar', name: 'ejercicio-editar', component: EjercicioForm, props: true, meta: { requiresAuth: true } },

    // Perfil
    { path: '/perfil', name: 'perfil', component: Perfil, meta: { requiresAuth: true } }, 
  ],
  scrollBehavior() {
    return { top: 0 }
  }
})

router.beforeEach((to, from) => {
  const auth = useAuthStore();
  if (to.meta?.requiresAuth && !auth.isLogged) {
    return { name: 'login', query: { redirect: to.fullPath } };
  }
});

export default router
