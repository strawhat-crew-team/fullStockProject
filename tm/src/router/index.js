// 路由表：url 路径 -> 页面组件映射
import {createRouter, createWebHistory} from 'vue-router'

import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Dashboard from '../views/Dashboard.vue'
import Tasks from '../views/Tasks.vue'

const routes = [
    {path: '/login', name: 'login', component: Login},
    {path: '/register', name: 'register', component: Register},
    {path: '/', name: 'dashboard', component: Dashboard},
    {path: '/tasks', name: 'tasks', component: Tasks}
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

// 路由守卫
router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('token')

    if(to.path === '/login' || to.path === '/register'){
        next()
    }else if(token) {
        next()
    }else{
        next('/login')
    }
})

export default router