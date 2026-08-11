// 全局请求出口：统一 baseURL，自动注入 token，处理错误

import axios from 'axios'


const http = axios.create({
    // 拿.env中的url前缀
    baseURL: import.meta.env.VITE_BASE_URL,
    timeout: 10000,
})

// 请求拦截器
http.interceptors.request.use((config) => {
    const token = localStorage.getItem('token')
    if (token) {
        config.headers.Authorization = `Bearer ${token}`
    }
    return config
})

// 响应拦截器：每次收到响应之后执行
http.interceptors.response.use(
    (response) => {
        return response.data
    },
    (error) => {
        // 响应错误
        if (error.response && error.response.status === 401) {
            // 跳转到登录页面
            localStorage.removeItem('token')
            window.location.href = '/login'
        }
        return Promise.reject(error)
    }
)

export default http