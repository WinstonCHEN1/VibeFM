import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import Floor from './pages/Floor.vue'
import FmPage from './pages/FmPage.vue'
import './style.css'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/',   name: 'floor', component: Floor },
    { path: '/fm', name: 'fm',    component: FmPage },
    { path: '/:pathMatch(.*)*', redirect: '/' },
  ],
  scrollBehavior() { return { top: 0 } },
})

createApp(App).use(createPinia()).use(router).mount('#app')
