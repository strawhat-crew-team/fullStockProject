# fullstock 项目开发流程

本文件记录整个项目（前端 + 后端）的**开发过程**与 **Git 操作**：先做什么、后做什么、为什么这个顺序、文件之间怎么联系。按开发顺序读，配合代码看。

## 一、文档分工

| 文档 | 作用 | 什么时候更新 |
|------|------|--------------|
| DEV.md | 项目蓝图 + 状态清单：技术栈、数据库设计、API 设计、Phase 进度勾选 | 结构/接口/进度变化时同步更新 |
| fullstock项目开发流程.md（本文件） | 开发**过程** + Git 操作手册：搭建命令、配置顺序、文件间联系、设计理由、git 全流程 | 每个 Phase 完成后补充对应部分 |

一句话：DEV.md 记录"做成什么样"，本文件记录"怎么做出来的"。

---

## 二、前端搭建流程（脚手架命令）

> 适用场景：只有 `01-GitHub_fullstock_project` 空文件夹，搭建前端项目骨架。
> 共 6 步，一行一行跑，每行都看输出。

### 第 1 步：进入项目根目录

```bash
cd "E:/python_project/后端开发学习/fastapi学习/01-GitHub_fullstock_project"
```

`cd`：change directory，切换当前工作目录。路径必须加双引号，因为包含中文和空格，不加引号会被拆成多段导致找不到目录。

### 第 2 步：用脚手架生成前端项目骨架

```bash
npm create vite@latest tm -- --template vue
```

拆解：

- `npm create vite@latest`：调用 Vite 官方脚手架，任何 `npm create xxx` 都表示"用 xxx 脚手架生成项目"
- `tm`：要创建的文件夹名（会生成 `tm/` 子目录）
- `--`：npm 的分隔符，表示后面的参数归 vite 管
- `--template vue`：指定 vue 模板（纯 JS 版；`vue-ts` 才是 TypeScript 版）

脚手架会自动生成：`package.json`、`index.html`、`vite.config.js`、`src/`、`public/`、`.gitignore` 等全部骨架文件，**不用手动建**。

### 第 3 步：进入前端目录

```bash
cd tm
```

后面所有操作都要在 tm 目录里进行。

### 第 4 步：装基础依赖

```bash
npm install
```

不带包名的 `npm install`：按 package.json 里的清单安装全部基础依赖（vue、vite、@vitejs/plugin-vue）。生成的 node_modules 目录存放这些依赖。

### 第 5 步：装业务依赖

```bash
npm install vue-router@4 axios element-plus
```

- `vue-router@4`：路由库，`@4` 锁大版本（Vue 3 配套的就是 v4）
- `axios`：HTTP 请求库
- `element-plus`：UI 组件库

装完后 package.json 的 `dependencies` 里会多出这三行，同时下载到 node_modules。

**为什么分两次装**：第 4 步是"项目本身需要的"（vue/vite），第 5 步是"业务功能需要的"（路由/请求/UI）。分开装能在 package.json 里清楚区分，这是团队项目惯例。

### 第 6 步：建业务目录

```bash
mkdir -p src/api src/router src/views
```

- `mkdir`：make directory，创建文件夹
- `-p`：parent，父目录不存在时自动创建；目录已存在时不报错
- `src/api`：放 axios 请求封装
- `src/router`：放路由配置
- `src/views`：放页面级组件（登录页、任务页等）

**为什么要手动建**：脚手架生成的是通用骨架（src/assets、src/components），任何 Vue 项目都一样。但 api/router/views 是项目自己的业务分层约定，脚手架无从知道，只能手动建。

### 验证骨架是否搭好

```bash
ls src/
```

应该看到：`api` `assets` `components` `router` `views`（以及 App.vue、main.js、style.css）。

### 骨架完成后的目录结构

```
01-GitHub_fullstock_project/
└── tm/                      ← 前端项目
    ├── src/                 ← 源代码
    │   ├── api/             ← axios 封装（第 6 步建）
    │   ├── assets/          ← 静态资源（脚手架生成）
    │   ├── components/      ← 通用组件（脚手架生成）
    │   ├── router/          ← 路由配置（第 6 步建）
    │   ├── views/           ← 页面组件（第 6 步建）
    │   ├── App.vue          ← 根组件（脚手架生成）
    │   ├── main.js          ← 应用入口（脚手架生成）
    │   └── style.css        ← 全局样式（脚手架生成）
    ├── node_modules/        ← 依赖包（第 4-5 步生成）
    ├── package.json         ← 依赖清单（脚手架生成）
    ├── vite.config.js       ← Vite 配置（脚手架生成）
    ├── index.html           ← 入口 HTML（脚手架生成）
    └── public/              ← 公共静态文件（脚手架生成）
```

### 后续开发步骤（不属于搭建）

骨架完成后进入配置环节，需要写：

- `vite.config.js`：配置 proxy 代理到后端 8008 端口
- `.env`：环境变量（后端地址）
- `src/api/http.js`：axios 封装（拦截器、token 注入）
- `src/router/index.js`：路由表
- `src/main.js`：挂载路由和 Element Plus
- `src/App.vue`：改为 router-view 容器
- `src/views/`：登录、注册、首页、任务页

详见下文「三、前端开发流程」和项目根目录 `DEV.md`。

---

## 三、前端开发流程（Phase 1 已完成）

### 0. 开发顺序总览

先配置文件（工具行为）→ 再基础代码（请求封装）→ 再页面（功能载体）→ 再入口（串联所有）→ 最后清理验证。

```
① 脚手架初始化（命令见第二章）
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

见第二章（Vite + Vue 3，纯 JS 不用 TS），结果：目录 `tm/`。

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

1. **代码结构变了 → 马上改 DEV.md 的项目结构图**（比如后端目录、复用环境的变更）。
2. **Phase 清单完成一项 → 勾一项**（代码写完就勾，不留到以后）。
3. **Phase 2 起：每写完一个后端接口 → 立即更新 DEV.md 的 API 设计表**（方法、路径、请求体、响应字段，以实际代码为准）。接口参数以"写出来的代码"为准，不以"最初的设计"为准——设计会变，文档必须跟代码走。
4. 本文件：每个 Phase 完成后再补一段（比如后端部分 Phase 2 完成后补）。

---

## 四、后端开发流程（Phase 2 进行中）

- [x] 环境：全局 Python 3.12（`C:\Users\lenovo\AppData\Local\Programs\Python\Python312`，已装 fastapi / uvicorn / sqlalchemy / PyJWT）；**所有后端命令必须先 `cd backend`**（模块 import 以启动目录为根，项目根跑会报 ModuleNotFoundError）
- [x] FastAPI 入口 main.py（8008 端口，lifespan 建表 + 挂载路由）
- [x] database.py（SQLite 引擎 / 会话 / Base）
- [x] models.py（user / task 表）
- [x] schemas.py（Pydantic 请求/响应模型）
- [x] auth.py（JWT 签发 create_token / 校验 decode_token / 依赖 get_current_user）
- [x] routers/auth.py（注册 / 登录接口）
- [ ] routers/tasks.py（任务 CRUD，用 Depends(get_current_user) 做身份识别）
- [ ] routers/stats.py（统计接口）
- [ ] requirements.txt（收尾时生成）
- [ ] 每完成一个接口同步更新 DEV.md 接口表
- [ ] 完成后补写本文件后端章节

---

## 五、Git 操作手册

### 1. 数据流动模型（核心概念）

数据在四个区域间流动：

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

其他概念：分支 = 指向某次提交的指针（main 是稳定版，dev/szdjf 是开发分支）；HEAD = 当前所在的分支；add/commit 都是纯本地操作，只有 push 才上网。

### 2. 仓库创建与第一次上传（完整命令清单）

时间点说明：**先完成第一次提交，再建开发分支**（无提交时分支不存在，`git branch` 会报错）。

#### 第 1 步：网页创建远程仓库

- 进入组织 `strawhat-crew-team` → New repository
- 仓库名：`fullStockProject`
- **不勾** README / .gitignore / license（勾了就会有一个初始提交，仓库就不是空的了，而我们要自己从零提交）
- Visibility：Public（公开，方便展示学习成果）

#### 第 2 步：本地初始化仓库（只做一次）

```bash
# 在项目根目录执行（01-GitHub_fullstock_project 下，不是 tm/ 里面！）
git init
# 作用：把当前目录变成仓库。目录里会多一个 .git 隐藏文件夹（仓库的心脏）。
# 位置 = 仓库边界：在这里 init，整个项目（前端 tm/、文档、backend/）都归这一个仓库管。
# 如果建在 tm/ 里面，根目录的文档和 backend/ 就管不到了（曾踩过这个坑，见"踩坑记录"）。

git config core.quotepath false
# 作用：让中文文件名正常显示。
# 默认情况下 git 会把中文文件名转义成 \351\241\271 这种八进制数字，开了这个就显示原文。
```

#### 第 3 步：创建 .gitignore（忽略不该提交的文件）

在根目录新建 `.gitignore` 文件，内容：

```
node_modules/    # 前端依赖包（几万个文件，npm install 能重新生成）
.venv/           # Python 虚拟环境（python -m venv 能重新生成）
__pycache__/     # Python 运行缓存
*.pyc
dist/            # 前端打包产物（npm run build 生成）
*.db             # SQLite 数据库文件（create_all 生成）
.env             # 前端环境变量
.idea/           # PyCharm 项目配置（每台电脑不一样，不该共享）
```

`git status` 时这些目录就不会再出现在"待提交清单"里了。

#### 第 4 步：第一次提交（在 main 上）

```bash
git add .
# 作用：把当前所有文件登记进暂存区（待提交清单）。
# 注意：add/commit 都是纯本地操作，还没传上网。

git commit -m "第一步：前端项目骨架"
# 作用：把暂存区内容存成一次提交（快照），-m 后面写这次干了啥。
# 提交完成后 main 分支才真正"存在"（分支 = 指向提交的指针，没有提交就没有分支）。
```

验证：`git log --oneline` 应该看到 `6957ca8 第一步：前端项目骨架`。

#### 第 5 步：创建开发分支

```bash
git checkout -b dev/szdjf
# 作用：新建分支 dev/szdjf 并切换过去。
# -b = branch，一条命令完成"新建 + 切换"。
# 分支规范：main 是主干（稳定版），dev/szdjf 是开发分支（日常开发都在这）。
```

验证：`git branch` 输出 `* dev/szdjf`（* = 当前所在分支）。

#### 第 6 步：关联远程仓库

```bash
git remote add origin https://github.com/strawhat-crew-team/fullStockProject.git
# 作用：给远程仓库地址起个名字叫 origin。
# origin 只是"名字"，不是"远程"本身（叫 abc 也行，只是行业惯例叫 origin）。
```

验证：`git remote -v` 能看到 origin 对应的地址。

#### 第 7 步：推送开发分支

```bash
git push -u origin dev/szdjf
# 作用：把本地 dev/szdjf 分支上传到远程创建同名分支。
# -u = upsteam，建立跟踪关系：以后直接 git pull 就能拉这个分支的更新。
# 推送成功后远程出现了 dev/szdjf，同时本地多了一条 remotes/origin/dev/szdjf。
```

**重点理解 `remotes/origin/dev/szdjf`**：它叫"远程跟踪分支"，只是你**本地**的一份"远程状态快照"，git 每次 fetch/push 自动更新。别人看不到它、它不能 checkout、删不掉也不用删。

#### 第 8 步：补推 main 主干（远程空仓库没有 main）

```bash
git push -u origin main
# 为什么需要这步：建仓库时没勾 README，远程是空仓库——没有任何提交，
# 也就没有任何分支（分支=指针原理，远程也一样）。网页上的"main"只是默认分支的"名字"，实际不存在。
# 因为没有 main，网页上 PR 的 base（目标分支）都选不了。
# 这步把本地 main 推上去，远程才有真正的主干分支。
```

#### 第 9 步：网页把默认分支改回 main

Settings（齿轮）→ Branches → Default branch → 选 `main` → Update

- 空仓库被 push 第一个分支后，GitHub 会自动把默认分支设成它（所以之前变成了 dev/szdjf）
- 默认分支 = 仓库设置里的"首页默认展示哪个分支"，跟分支本身是两回事

#### 第 10 步：验证收尾

```bash
git fetch
# 作用：把远程的最新状态拉回本地，更新远程跟踪分支。

git branch -a
# 作用：列出所有分支。看到这三行就对了：
#   * main                    ← 本地主干，当前所在
#     remotes/origin/dev/szdjf  ← 远程 dev 的本地快照
#     remotes/origin/main       ← 远程 main 的本地快照（出现 = 第 8 步成功）
```

### 3. 关键概念

| 概念 | 一句话解释 |
|------|-----------|
| 仓库边界 | `git init` 的位置决定这个仓库管哪些文件，一个项目只 init 一次 |
| 分支 = 指针 | 分支只是指向某次提交的箭头，没有提交就没有分支 |
| 暂存区 | `git add` 后的"待提交清单"，commit 前可以反悔 |
| 本地 vs 远程 | add/commit 纯本地，只有 push 才上网 |
| 远程跟踪分支 | `remotes/origin/xxx` = 本地保存的远程快照，自动维护 |
| 默认分支 | 仓库设置，显示在网页首页的分支，可随时改 |
| PR 的时机 | main 与 dev 内容相同（nothing to compare）时没有合并意义，等 dev 领先 main 有真实差异再走 PR |
| push 被拒 | 远程有本地没有的提交时拒绝（保护机制防覆盖），先 pull 再 push，禁止 force push |

### 4. 踩坑记录（实际遇到的）

1. **在 tm/ 子目录里 git init 了** → 仓库边界错了，根目录文档管不到。修复：删掉 tm/.git（无提交零损失，回收站删除），回到根目录重新 init。
2. **git branch 报 "not a valid object name: 'main'"** → 还没有任何提交，分支不存在。修复：先在 main 上做第一次 commit，再建开发分支。
3. **git status 中文文件名显示成八进制**（`fullstock\351\241\271...`）→ 不是损坏，git 默认转义非 ASCII 文件名。修复：`git config core.quotepath false`。
4. **git add 时大量 "LF will be replaced by CRLF" 警告** → Windows 换行符转换提示，无害，不用处理。
5. **fetch/push 报 "Connection was reset"** → GitHub 网络波动，重试即可。
6. **远程没有 main 分支** → 空仓库（未勾 README）无分支，首个 push 的分支被自动设为默认分支。修复：push main + 网页改默认分支。
7. **push 被拒（rejected）** → 远程分支有本地没有的提交（比如自己在网页合并了 PR）。处理：`git pull origin <分支>` 拉下来合并，再 `git push`。诊断命令：`git log HEAD..origin/<分支> --pretty=format:"%h|%an|%ad|%s"`（%an 看是谁的提交——网页操作作者是 GitHub 账号名，不是本地 git config 名）。
8. **git 身份是占位符** → 教程复制的 "Your GitHub Username" 不是真实身份。修复：`git config user.name "真实名"` + `git config user.email "真实邮箱"`（仓库级配置，配置成功无输出 = 成功）。

### 5. 日常循环与提交习惯（以后 80% 时间只用的 4 条）

```bash
git status             # 看状态：改了什么、哪些没登记
git add .              # 登记所有改动进暂存区
git commit -m "说明"    # 存档，说明写清楚这次干了啥
git push               # 同步到远程仓库（已建立跟踪的分支直接 push）
```

习惯：**每完成一个小任务（一个文件/一个接口/一个页面）→ commit 一次**，一个 commit 只做一件事；每个 Phase 完成 → push + 网页发起 PR 合入 main。

### 6. 命令速查表

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
| `git fetch` | 把远程最新状态拉回本地（不合并） |
| `git remote -v` | 查看远程仓库地址 |
| `git diff` | 看还没登记的改动内容 |
| `git log HEAD..origin/<分支>` | 看远程有而本地没有的提交（push 被拒时诊断） |

仓库实时状态看 `git status` / `git log` / 网页，文档不记录实时状态（容易过期）。
