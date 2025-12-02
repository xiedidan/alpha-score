import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/pages/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    name: 'Main',
    component: () => import('@/layouts/MainLayout.vue'),
    redirect: '/dashboard',
    meta: { requiresAuth: true },
    children: [
      {
        path: '/dashboard',
        name: 'Dashboard',
        component: () => import('@/pages/Dashboard.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: '/trading',
        name: 'Trading',
        component: () => import('@/pages/Trading.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: '/config',
        name: 'Config',
        component: () => import('@/pages/Config.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: '/history',
        name: 'History',
        component: () => import('@/pages/History.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: '/logs',
        name: 'Logs',
        component: () => import('@/pages/Logs.vue'),
        meta: { requiresAuth: true }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// Navigation guard for authentication
router.beforeEach((to, _from, next) => {
  const isAuthenticated = !!localStorage.getItem('token')

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else if (to.path === '/login' && isAuthenticated) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
