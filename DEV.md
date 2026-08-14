# tm 项目开发文档

## 项目概述

时间管理应用（Time Management），前后端分离架构。前端 Vue 3 + Element Plus，后端 FastAPI + SQLite。

## 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| 前端框架 | Vue 3 (JS) | 组合式 API，script setup 语法 |
| 构建工具 | Vite | 开发服务器 + 打包 |
| 路由 | vue-router 4 | 前端路由管理 |
| HTTP | axios | 请求封装 + 拦截器 |
| UI 组件 | Element Plus | 按钮/表单/表格/消息提示 |
| 后端框架 | FastAPI | Python 异步 Web 框架 |
| 数据库 | SQLite | 轻量级关系数据库 |
| ORM | SQLAlchemy | 数据库对象映射 |
| 认证 | JWT (HS256) | 登录态管理 |
| 建表方式 | create_all (Base.metadata) | 开发期启动时自动建表，暂不引入迁移工具 |

## 项目结构

```
01-GitHub_fullstock_project/
├── DEV.md                 # 项目开发文档（本文件）
├── fullstock项目开发流程.md  # 开发过程 + Git 操作手册（含前端搭建步骤）
├── tm/                    # 前端项目
│   ├── index.html         # 入口 HTML
│   ├── package.json       # 依赖清单
│   ├── vite.config.js     # Vite 配置（proxy 代理到 8008）
│   ├── .env               # 环境变量（VITE_API_BASE_URL=/api）
│   ├── .gitignore         # git 忽略清单
│   ├── public/            # 静态资源（不编译，原样复制）
│   │   └── favicon.svg    # 网站图标
│   └── src/
│       ├── main.js        # 应用入口（挂载 Vue + 路由 + Element Plus）
│       ├── App.vue        # 根组件（router-view 容器）
│       ├── style.css      # 全局样式
│       ├── api/
│       │   └── http.js    # axios 封装（实例/拦截器/token注入）
│       ├── router/
│       │   └── index.js   # 路由表定义 + 全局守卫（未登录踢回 /login）
│       ├── views/         # 页面级组件
│       │   ├── Login.vue      # 登录页
│       │   ├── Register.vue   # 注册页
│       │   ├── Dashboard.vue  # 首页/概览
│       │   └── Tasks.vue      # 任务管理页
│       ├── components/    # 可复用组件（当前为空）
│       └── assets/        # 编译资源（当前为空）
└── backend/               # 后端项目（Phase 2 开发中）
    ├── main.py            # FastAPI 入口，8008 端口（✅ 已完成）
    ├── database.py        # SQLite 引擎 / 会话 / 公共基类 Base（✅ 已完成）
    ├── models.py          # ORM 模型 User / Task 两张表（✅ 已完成）
    ├── schemas.py         # Pydantic 请求/响应模型（✅ 已完成）
    ├── auth.py            # JWT 签发与校验工具（✅ 已完成）
    ├── routers/           # 路由模块
    │   ├── auth.py        # 注册 / 登录（✅ 已完成）
    │   ├── tasks.py       # 任务 CRUD（✅ 已完成）
    │   └── stats.py       # 统计（✅ 已完成）
    ├── tm.db              # SQLite 数据文件（运行时生成，已 git 忽略）
    └── requirements.txt   # 依赖清单（✅ 已生成）
    # Python 环境：全局 Python 3.12（C:\Users\lenovo\AppData\Local\Programs\Python\Python312，
    # 已装 fastapi / uvicorn / sqlalchemy / PyJWT）
```

## 数据库设计

### user 表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer (PK, 自增) | 用户ID |
| phone | String (唯一) | 手机号，登录账号 |
| password | String | 密码（学习阶段明文，生产须哈希） |
| nickname | String | 昵称 |
| is_admin | Boolean | 是否管理员 |
| created_at | DateTime | 注册时间 |

### task 表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer (PK, 自增) | 任务ID |
| user_id | Integer (FK→user.id) | 所属用户 |
| code | String | 任务编号 |
| subject | String | 任务主题 |
| sub_task | String | 子任务描述 |
| target_hours | Float | 目标工时 |
| plan_hours | Float | 计划工时 |
| start_time | DateTime | 开始时间 |
| end_time | DateTime | 结束时间 |
| actual_hours | Float | 实际工时 |
| date | Date | 日期 |
| is_archived | Boolean | 是否归档 |
| created_at | DateTime | 创建时间 |

## API 设计

### 认证模块 `/api`

| 方法 | 路径 | 说明 | 请求体 | 响应 |
|------|------|------|--------|------|
| GET | / | 探活 | - | { message } |
| POST | /api/register | 注册 | phone, password, nickname | { message } |
| POST | /api/login | 登录 | phone, password | { access_token, token_type } |

### 任务模块 `/api/tasks`（需 JWT）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/tasks | 获取当前用户任务列表 |
| POST | /api/tasks | 创建任务 |
| PUT | /api/tasks/{id} | 更新任务 |
| DELETE | /api/tasks/{id} | 删除任务 |
| POST | /api/tasks/{id}/archive | 归档任务 |

### 统计模块 `/api/stats`（需 JWT）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/stats/daily | 每日工时统计 |
| GET | /api/stats/efficiency | 任务完成率 |

## 前端路由

| 路径 | 组件 | 说明 |
|------|------|------|
| /login | Login | 登录页（未登录默认跳转） |
| /register | Register | 注册页 |
| / | Dashboard | 首页概览（需登录） |
| /tasks | Tasks | 任务管理（需登录） |

## 开发阶段

### Phase 1：项目骨架 ✅ 已完成
- [x] Vite + Vue 3 项目初始化
- [x] 安装 vue-router / axios / element-plus
- [x] 创建目录结构（api/ router/ views/）
- [x] vite.config.js 配置 proxy 代理到后端 8008 端口
- [x] .env 环境变量配置
- [x] 配置路由表 router/index.js
- [x] 封装 axios 实例 api/http.js
- [x] main.js 挂载路由和 Element Plus
- [x] 创建空白页面组件（Login / Register / Dashboard / Tasks）
- [x] App.vue 改为 router-view 容器

### Phase 2：后端搭建
- [x] FastAPI 入口 main.py（8008 端口）
- [x] 数据库连接 database.py（SQLite 引擎 / 会话 / Base）
- [x] SQLAlchemy 模型定义 models.py（user / task 表）
- [x] Pydantic 请求/响应模型 schemas.py
- [x] JWT 认证（注册/登录接口）
- [x] 任务 CRUD 接口
- [x] 统计接口
- [x] requirements.txt

### Phase 3：登录联调 ✅ 已完成
- [x] 前端登录页 UI（el-form 校验 + 登录请求 + token 存储）
- [x] 注册页 UI（自定义 validator 校验两次密码一致）
- [x] axios 拦截器注入 token（http.js）
- [x] 路由守卫（未登录跳转 /login，router/index.js）
- [x] 前后端联调通过（注册/登录/守卫三环节实测）
- [x] 修复 vite.config.js：sever→server、api→/api、https→http

### Phase 4：任务管理
- [ ] 任务列表页（表格 + 筛选）
- [ ] 创建/编辑任务表单
- [ ] 删除 + 归档功能
- [ ] Element Plus 组件集成

### Phase 5：统计与优化
- [ ] Dashboard 统计卡片
- [ ] ECharts 图表（工时趋势 / 完成率）
- [ ] 响应式布局优化
- [ ] 部署准备

## 环境要求

- Node.js >= 18
- Python >= 3.12
- npm（Node 自带）

## 启动命令

```bash
# 前端开发服务器（端口 5173）
cd tm
npm run dev

# 后端（端口 8008，用全局 Python 3.12，已装 fastapi/uvicorn/sqlalchemy/PyJWT）
cd backend
C:/Users/lenovo/AppData/Local/Programs/Python/Python312/python.exe -m uvicorn main:app --reload --port 8008
```

## 约定

- 前端代码用纯 JS，不用 TypeScript
- 注释按教学标准写：语法格式优先，每个参数解释，写"为什么"不只"怎么做"
- 后端返回纯 JWT（不带 Bearer 前缀），前端拦截器负责拼接
- API 路径统一 `/api` 前缀，vite proxy 代理转发
- Git 分支规范：dev 开发 → PR 合入 master
- 每完成一个后端文件或接口，立即更新本文件（目录结构 / 接口表 / 开发进度）
