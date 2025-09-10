import { createRouter, createWebHistory } from 'vue-router'

const Home = () => import('../views/Home.vue')
const About = () => import('../views/About.vue')
const Contact = () => import('../views/Contact.vue')
const EjercicioDetalle = () => import('../views/EjercicioDetalle.vue')
const Login = () => import('../views/Login.vue');
const Register = () => import('../views/Register.vue');

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'home', component: Home },
    { path: '/about', name: 'about', component: About },
    { path: '/contact', name: 'contact', component: Contact },
    { path: '/ejercicio/:slug', name: 'ejercicio-detalle', component: EjercicioDetalle, props: true },
    { path: '/login', name: 'login', component: Login },
    { path: '/register', name: 'register', component: Register },
  ],
  scrollBehavior() {
    return { top: 0 }
  }
})

export default router
