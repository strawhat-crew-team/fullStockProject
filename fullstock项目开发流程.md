# fullstock 项目开发流程

本文件记录整个项目（前端 + 后端）的**开发过程**：先做什么、后做什么、为什么这个顺序、文件之间怎么联系。按开发顺序读，配合代码看。

## 一、文档分工（三个文档别搞混）

| 文档 | 作用 | 什么时候更新 |
|------|------|--------------|
| DEV.md | 项目蓝图 + 状态清单：技术栈、数据库设计、API 设计、Phase 进度勾选 | 结构/接口/进度变化时同步更新 |
| 前端搭建流程.md | 脚手架搭建的**命令**步骤（npm create vite 到目录创建） | 一次性，建完就不用动 |
| fullstock项目开发流程.md（本文件） | 开发**过程**：文件配置顺序、文件间联系、设计理由 | 每个 Phase 完成后补充对应部分 |

一句话：DEV.md 记录"做成什么样"，本文件记录"怎么做出来的"。

## 二、前端开发流程（Phase 1 已完成）

### 0. 开发顺序总览

先配置文件（工具行为）→ 再基础代码（请求封装）→ 再页面（功能载体）→ 再入口（串联所有）→ 最后清理验证。

```
① 脚手架初始化（命令见前端搭建流程.md）
② 安装依赖 vue-router / axios / element-plus
③ vite.config.js        代理规则（前端配置文件）
④ .env                  环境变量（前端配置文件）
⑤ 创建目录结构 api/ router/ views/
⑥ api/http.js          axios 封装（先于页面，页面要 import 它）
⑦ router/index.js      路由表（先于页面，它 import 页面）
⑧ views/ 四个空白页面   （页面本身）
⑨ main.js              入口（它 import 了 ⑥⑦ 和 App.vue）
⑩ App.vue              根组件（路由出口）
⑪ 删除脚手架残留文件
⑫ npm run dev 启动验证
```

为什么这个顺序：③④ 是工具配置不依赖任何代码，先配好；⑥⑦ 是"服务层"，页面要 import 它们所以先写；⑧ 页面是被 ⑦ import 的，所以 ⑦⑧ 顺序反过来也不报错（vite 编译时才找文件）；⑨ main.js 是唯一"引用一切"的文件，所以放最后；⑩ 根组件只放一个 router-view；⑪ 必须等 ⑩ 改完才能删（原因见 11 节）。

### 1. 脚手架初始化

见《前端搭建流程.md》，结果：Vite + Vue 3（纯 JS，不用 TS）项目，目录 `tm/`。

### 2. 安装依赖

```
npm install vue-router@4 axios element-plus
```

三个包的作用：vue-router 管路由（URL ↔ 页面映射）、axios 发 HTTP 请求、element-plus 是现成 UI 组件库（按钮/表单/表格）。

### 3. vite.config.js —— 代理规则

```js
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8008',  // 后端地址
      changeOrigin: true,                // 改写 Host 请求头
    },
  },
}
```

作用：浏览器里请求 `/api/xxx` → 发到前端 5173 → vite 进程内部转发给后端 8008 → 响应原路返回。这样前端代码里写相对路径 `/api` 就行，不用管后端地址，且避开了浏览器的同源策略（5173 和 8008 端口不同，直接跨域）。

### 4. .env —— 环境变量

```js
VITE_API_BASE_URL=/api
```

规则：只有 `VITE_` 前缀的变量才会暴露给前端代码；代码里用 `import.meta.env.VITE_API_BASE_URL` 读取。写成相对路径 `/api` 而不是绝对地址，是为了配合第 3 节的代理（写绝对地址会绕过代理直连 8008，遇到跨域；且部署换地址要改代码）。

### 5. 目录结构

```
src/
├── api/       接口层：所有和后端通信的代码
├── router/    路由层：URL 和页面的映射
├── views/     页面组件：一个页面一个文件，和路由一一对应
├── components/ 可复用小组件（当前为空，后续填充）
└── assets/    编译资源（当前为空，后续填充）
```

命名约定：文件夹小写按职责分；组件文件名首字母大写（文件名即组件名，大写和 HTML 原生标签区分）。

### 6. api/http.js —— axios 封装

```js
const http = axios.create({ baseURL: import.meta.env.VITE_API_BASE_URL, timeout: 10000 })
// 请求拦截器：从 localStorage 取 token，拼成 "Bearer xxx" 加进请求头
// 响应拦截器：成功时剥壳返回 response.data；401 时清 token 并跳转 /login
export default http
```

作用：所有页面发请求都 `import http`，统一走这一个实例——统一加 token、统一处理错误，不用每个页面重复写。**这就是"封装"的意义**。

### 7. router/index.js —— 路由表

```js
{ path: '/login', name: 'login', component: Login }      // 登录页
{ path: '/register', name: 'register', component: Register }  // 注册页
{ path: '/', name: 'dashboard', component: Dashboard }   // 仪表盘（登录后主页）
{ path: '/tasks', name: 'tasks', component: Tasks }      // 任务管理页
```

用 `createWebHistory()`：URL 无 # 号（干净）。注意：生产部署后直接刷新子路径（如 /tasks）需要服务器配"所有路径重定向到 index.html"，否则 404；开发环境 vite 已自动处理。

### 8. views/ 四个空白页面

每个文件只有 `<template><div><h1>占位文字</h1></div></template>` 三块结构（template 结构 / script setup 逻辑 / style scoped 样式）。先建空壳的意义：让路由 import 不报错、让项目能跑起来，页面内容 Phase 3/4 再填。

### 9. main.js —— 入口（串联一切）

```js
import { createApp } from 'vue'
import router from './router/index.js'
import ElementPlus from 'element-plus'            // UI 组件库
import zhCn from 'element-plus/es/locale/lang/zh-cn'  // 中文语言包

const app = createApp(App)
app.use(router)                                  // 注册路由
app.use(ElementPlus, { locale: zhCn })           // 注册组件库
app.mount('#app')
```

要点：`app.use()` 是"给应用装插件"，router 和 ElementPlus 都是插件；装完以后全局生效——任何页面直接写 `<el-button>`、`<router-view>` 不用再 import（这就是"全局注册"）。

### 10. App.vue —— 根组件（路由出口）

```vue
<template>
  <router-view />
</template>
```

只有这一行：router-view 是"位置标记"，当前 URL 对应的页面组件渲染到这里。App.vue 是整棵组件树的根，只负责占位。

### 11. 删除脚手架残留（时机很重要）

**删除时机**：必须等 App.vue 改完（不再 import HelloWorld 和图片）之后，此时这些文件没有任何引用了，删了不报编译错。

删 5 个：`src/components/HelloWorld.vue`、`src/assets/vite.svg`、`src/assets/vue.svg`、`src/assets/hero.png`、`public/icons.svg`。

保留 1 个：`public/favicon.svg`（index.html 直接引用，删了 404）。

验证方法：全局搜索（Ctrl+Shift+F）搜 `HelloWorld`、`vite.svg`、`vue.svg`、`hero.png`、`icons.svg`，0 结果 = 干净。

**判断"文件能不能删"的通用规则**：搜全项目还有没有文件引用它；没有引用就能删。

### 12. 启动验证

```
cd tm && npm run dev
```

终端保持运行，浏览器访问四个地址验证路由：`/` → 仪表盘、`/login` → Login、`/register` → Register、`/tasks` → 任务管理。全部正常 = Phase 1 完成。

### 前端文件依赖链（横向联系）

```
index.html（浏览器入口）
  └─ <script src="/src/main.js">         ← 唯一入口 JS
       ├─ import App.vue                 ← 根组件
       │    └─ <router-view>             ← 路由出口
       │         └─ router/index.js      ← 路由表（import 了 4 个页面）
       │              └─ views/*.vue     ← 页面组件
       ├─ import router                  ← 同上，注册到应用
       └─ import ElementPlus             ← UI 组件库（全局注册）
页面组件 ──import──> api/http.js          ← 请求封装（发后端请求都走它）
```

依赖方向永远是"入口引用功能"，页面之间不互相 import（页面是平级的）。

### 与 DEV.md 的同步规则（重点）

1. **代码结构变了 → 马上改 DEV.md 的项目结构图**（比如这次后端目录、复用环境的变更）。
2. **Phase 清单完成一项 → 勾一项**（代码写完就勾，不留到以后）。
3. **Phase 2 起：每写完一个后端接口 → 立即更新 DEV.md 的 API 设计表**（方法、路径、请求体、响应字段，以实际代码为准）。接口参数以"写出来的代码"为准，不以"最初的设计"为准——设计会变，文档必须跟代码走。
4. 本文件：每个 Phase 完成后再补一段（比如后端部分 Phase 2 完成后补）。

## 三、后端开发流程（Phase 2 开始后补充）

- [ ] 环境准备：复用 `E:\python_project\.venv`（Python 3.12.1），激活：PowerShell 执行 `E:\python_project\.venv\Scripts\Activate.ps1`
- [ ] FastAPI 项目结构（backend/ 目录）
- [ ] 数据库模型、JWT 认证、任务 CRUD、统计接口（按 DEV.md 设计）
- [ ] 每完成一个接口同步更新 DEV.md 接口表
- [ ] 完成后补写本文件后端章节

## 四、Git 常用命令速查与提交习惯

### 1. 核心模型：数据在四个区域间流动

```
工作区（你正在编辑的文件）
   │  git add           ← 登记
   ▼
暂存区（待提交清单）
   │  git commit        ← 存档
   ▼
本地仓库（提交历史，每次存档是一个快照）
   │  git push          ← 上传
   ▼
远程仓库（GitHub 上的备份）
```

其他概念：分支 = 指向某次提交的指针（main 是稳定版，dev/szdjf 是开发分支）；HEAD = 当前所在的分支。

### 2. 日常循环（80% 时间只用的 4 条命令）

```
git status             # 看状态：改了什么、哪些没登记
git add .              # 登记所有改动进暂存区
git commit -m "说明"    # 存档，说明写清楚这次干了啥
git push               # 同步到远程仓库
```

### 3. 命令速查表

| 命令 | 作用 |
|------|------|
| `git init` | 目录变成仓库（一个项目只做一次） |
| `git status` | 查看状态（最常用） |
| `git add <文件>` 或 `git add .` | 登记改动到暂存区 |
| `git commit -m "说明"` | 存档 |
| `git log --oneline` | 看提交历史，一行一条 |
| `git branch` | 看分支列表，`*` 是当前所在 |
| `git checkout <分支名>` | 切换到已有分支 |
| `git checkout -b <分支名>` | 新建分支并切过去 |
| `git push` | 本地提交推到远程 |
| `git pull` | 远程新改动拉到本地（协作时用） |
| `git remote -v` | 查看远程仓库地址 |

### 4. 提交习惯（学习计划的一部分）

- 每完成一个小任务（一个文件 / 一个接口 / 一个页面）→ commit 一次，说明写清楚
- commit 前先 `git status` 看自己改了什么
- 每个 Phase 完成 → `git push` + 网页发起 PR 合入 main
- 命令里的分支名：本项目约定主分支 `main`、开发分支 `dev/szdjf`

