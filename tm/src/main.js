//  浏览器加载 index.html 后，就从这里的代码开始执行
//  凡是"整个项目都要用"的东西（路由、UI 组件库），都在这里注册

// Vue提供的函数，创建"应用实例"
import { createApp } from 'vue'

// 引入路由
import router from './router/index.js'

// Element Plus: UI 组件库。按钮 输入框 表格都来自它
import ElementPlus from 'element-plus'

// 组件仓库配套演示文件，不引入组件是"裸"的
import 'element-plus/dist/index.css'

// 中文语言包。组件自带的文字（比如分页器）默认是英文，传这个包就变中文
import zhCn from 'element-plus/es/locale/lang/zh-cn'

import './style.css'

// 所有页面都挂在他下面，他负责显示“当前路由对应的页面”
import App from './App.vue'

// 创建应用实例
const app = createApp(App)

app.use(router) // 挂载路由
app.use(ElementPlus, {locale: zhCn})  // 安装

// 将应用渲染到index.html中
app.mount('#app')
