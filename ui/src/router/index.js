import { createRouter, createWebHashHistory } from 'vue-router'

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    { path: '/', component: () => import('../views/index/Index.vue') },
    { path: '/ai', component: () => import('../views/ai/index/Index.vue') },
    { path: '/ai/chat', component: () => import('../views/ai/chat/Chat.vue') },
    { path: '/map', component: () => import('../views/map/Map.vue') },
  ],
})

export default router
