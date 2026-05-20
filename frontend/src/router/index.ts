import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: '登录',
    component: () => import('../views/LoginPage.vue')
  },
  {
    path: '/register',
    name: '注册',
    component: () => import('../views/RegisterPage.vue')
  },
  {
    path: '/forgot-password',
    name: '忘记密码',
    component: () => import('../views/ForgotPasswordPage.vue')
  },
  {
    path: '/',
    component: () => import('../views/MainLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: 'detection',
        name: '智能检测',
        component: () => import('../views/DetectionPage.vue'),
        meta: { title: '智能检测' }
      },
      {
        path: 'history',
        name: '历史记录',
        component: () => import('../views/HistoryPage.vue'),
        meta: { title: '历史记录' }
      },
      {
        path: 'qa',
        name: 'AI问答',
        component: () => import('../views/QAPage.vue'),
        meta: { title: 'AI问答' }
      },
      {
        path: 'targets',
        name: '目标库',
        component: () => import('../views/TargetsPage.vue'),
        meta: { title: '目标库' }
      },
      {
        path: 'profile',
        name: '个人中心',
        component: () => import('../views/ProfilePage.vue'),
        meta: { title: '个人中心' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const authPaths = ['/login', '/register', '/forgot-password']

  if (authPaths.includes(to.path)) {
    if (token && to.path === '/login') {
      next('/detection')
    } else {
      next()
    }
  } else if (!token) {
    next('/login')
  } else {
    next()
  }
})

export default router
