import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],

  sever: {
    proxy: {
      // 请求路径前缀/api/xxx 会被代理到 https://localhost:8000/xxx
      'api': {
        // 浏览器往哪里发请求
        target: 'https://localhost:8008',
        //
        changeOrigin: true,
      }
    }
  }
})
