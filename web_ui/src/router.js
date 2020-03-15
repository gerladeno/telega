import Vue from 'vue'
import Router from 'vue-router'
import store from './store/store'

Vue.use(Router)

const router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Master',
      meta: {
        layout: 'MainLayout',
        requiresAuth: true
      },
      component: () => import('./views/Master.vue')
    },
    {
      path: '/login',
      name: 'login',
      meta: {
        layout: 'EmptyLayout',
        authRequered: false
      },
      component: () => import('./views/Login.vue'),
      beforeEnter: (to, from, next) => {
        if (store.getters['session/isValid']) {
          next({
            name: 'Master'
          })
        }
        else {
          next()
        }
      }
    },
    {
      path: '/logout',
      name: 'logout',
      meta: {
        layout: 'EmptyLayout',
        authRequered: true
      },
      component: () => import('./components/Logout.vue')
    }
  ]
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!store.getters['session/isValid']) {
      next({
        path: '/login'
      })
    } else {
      next()
    }
  } else {
    next() // всегда так или иначе нужно вызвать next()!
  }
})

export default router