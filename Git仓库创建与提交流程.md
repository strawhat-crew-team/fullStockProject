# Git 仓库创建与提交流程（Phase 1 完整记录）

> 本文档记录从「网页创建仓库」到「Phase 1 上传完毕」的完整 git 操作流程。
> 每步都带注释说明"为什么"，以后重新初始化仓库时可以照着走。

---

## 一、流程总览

```
网页建仓库 → 本地 git init → 配 .gitignore → 第一次 commit
→ 建开发分支 dev/szdjf → 关联远程 origin → push dev/szdjf
→ 补 push main → 网页改默认分支 → fetch 验证
```

时间点说明：**先完成第一次提交，再建开发分支**（无提交时分支不存在，`git branch` 会报错）。

---

## 二、完整命令清单（带注释）

### 第 1 步：网页创建远程仓库

- 进入组织 `strawhat-crew-team` → New repository
- 仓库名：`fullStockProject`
- **不勾** README / .gitignore / license（勾了就会有一个初始提交，仓库就不是空的了，而我们要自己从零提交）
- Visibility：Public（公开，方便展示学习成果）

### 第 2 步：本地初始化仓库（只做一次）

```bash
# 在项目根目录执行（01-GitHub_fullstock_project 下，不是 tm/ 里面！）
git init
# 作用：把当前目录变成仓库。目录里会多一个 .git 隐藏文件夹（仓库的心脏）。
# 位置 = 仓库边界：在这里 init，整个项目（前端 tm/、文档、以后的 backend/）都归这一个仓库管。
# 如果建在 tm/ 里面，根目录的文档和 backend/ 就管不到了（曾踩过这个坑，见"踩坑记录"）。

git config core.quotepath false
# 作用：让中文文件名正常显示。
# 默认情况下 git 会把中文文件名转义成 \351\241\271 这种八进制数字，开了这个就显示原文。
```

### 第 3 步：创建 .gitignore（忽略不该提交的文件）

在根目录新建 `.gitignore` 文件，内容：

```
node_modules/    # 前端依赖包（几万个文件，npm install 能重新生成）
.venv/           # Python 虚拟环境（python -m venv 能重新生成）
__pycache__/     # Python 运行缓存
*.pyc
dist/            # 前端打包产物（npm run build 生成）
```

`git status` 时这些目录就不会再出现在"待提交清单"里了。

### 第 4 步：第一次提交（在 main 上）

```bash
git add .
# 作用：把当前所有文件登记进暂存区（待提交清单）。
# 注意：add/commit 都是纯本地操作，还没传上网。

git commit -m "第一步：前端项目骨架"
# 作用：把暂存区内容存成一次提交（快照），-m 后面写这次干了啥。
# 提交完成后 main 分支才真正"存在"（分支 = 指向提交的指针，没有提交就没有分支）。
```

验证：`git log --oneline` 应该看到 `6957ca8 第一步：前端项目骨架`。

### 第 5 步：创建开发分支

```bash
git checkout -b dev/szdjf
# 作用：新建分支 dev/szdjf 并切换过去。
# -b = branch，一条命令完成"新建 + 切换"。
# 分支规范：main 是主干（稳定版），dev/szdjf 是开发分支（日常开发都在这）。
```

验证：`git branch` 输出 `* dev/szdjf`（* = 当前所在分支）。

### 第 6 步：关联远程仓库

```bash
git remote add origin https://github.com/strawhat-crew-team/fullStockProject.git
# 作用：给远程仓库地址起个名字叫 origin。
# origin 只是"名字"，不是"远程"本身（叫 abc 也行，只是行业惯例叫 origin）。
```

验证：`git remote -v` 能看到 origin 对应的地址。

### 第 7 步：推送开发分支

```bash
git push -u origin dev/szdjf
# 作用：把本地 dev/szdjf 分支上传到远程创建同名分支。
# -u = upsteam，建立跟踪关系：以后直接 git pull 就能拉这个分支的更新。
# 推送成功后远程出现了 dev/szdjf，同时本地多了一条 remotes/origin/dev/szdjf。
```

**重点理解 `remotes/origin/dev/szdjf`**：它叫"远程跟踪分支"，只是你**本地**的一份"远程状态快照"，git 每次 fetch/push 自动更新。别人看不到它、它不能 checkout、删不掉也不用删。

### 第 8 步：补推 main 主干（远程空仓库没有 main）

```bash
git push -u origin main
# 为什么需要这步：建仓库时没勾 README，远程是空仓库——没有任何提交，
# 也就没有任何分支（分支=指针原理，远程也一样）。网页上的"main"只是默认分支的"名字"，实际不存在。
# 因为没有 main，网页上 PR 的 base（目标分支）都选不了。
# 这步把本地 main 推上去，远程才有真正的主干分支。
```

### 第 9 步：网页把默认分支改回 main

Settings（齿轮）→ Branches → Default branch → 选 `main` → Update

- 空仓库被 push 第一个分支后，GitHub 会自动把默认分支设成它（所以之前变成了 dev/szdjf）
- 默认分支 = 仓库设置里的"首页默认展示哪个分支"，跟分支本身是两回事

### 第 10 步：验证收尾

```bash
git fetch
# 作用：把远程的最新状态拉回本地，更新远程跟踪分支。

git branch -a
# 作用：列出所有分支。看到这三行就对了：
#   * main                    ← 本地主干，当前所在
#     remotes/origin/dev/szdjf  ← 远程 dev 的本地快照
#     remotes/origin/main       ← 远程 main 的本地快照（出现 = 第 8 步成功）
```

---

## 三、这次的关键概念

| 概念 | 一句话解释 |
|------|-----------|
| 仓库边界 | `git init` 的位置决定这个仓库管哪些文件，一个项目只 init 一次 |
| 分支 = 指针 | 分支只是指向某次提交的箭头，没有提交就没有分支 |
| 暂存区 | `git add` 后的"待提交清单"，commit 前可以反悔 |
| 本地 vs 远程 | add/commit 纯本地，只有 push 才上网 |
| 远程跟踪分支 | `remotes/origin/xxx` = 本地保存的远程快照，自动维护 |
| 默认分支 | 仓库设置，显示在网页首页的分支，可随时改 |
| PR 的时机 | main 与 dev 内容相同（nothing to compare）时没有合并意义，等 dev 领先 main 有真实差异再走 PR |

---

## 四、踩坑记录（这次实际遇到的）

1. **在 tm/ 子目录里 git init 了** → 仓库边界错了，根目录文档管不到。修复：删掉 tm/.git（无提交零损失，回收站删除），回到根目录重新 init。
2. **git branch 报 "not a valid object name: 'main'"** → 还没有任何提交，分支不存在。修复：先在 main 上做第一次 commit，再建开发分支。
3. **git status 中文文件名显示成八进制**（`fullstock\351\241\271...`）→ 不是损坏，git 默认转义非 ASCII 文件名。修复：`git config core.quotepath false`。
4. **git add 时大量 "LF will be replaced by CRLF" 警告** → Windows 换行符转换提示，无害，不用处理。
5. **fetch/push 报 "Connection was reset"** → GitHub 网络波动，重试即可。
6. **远程没有 main 分支** → 空仓库（未勾 README）无分支，首个 push 的分支被自动设为默认分支。修复：push main + 网页改默认分支。

---

## 五、日常循环（以后 80% 时间只用的 4 条）

```bash
git status             # 看状态：改了什么、哪些没登记
git add .              # 登记所有改动进暂存区
git commit -m "说明"    # 存档，说明写清楚这次干了啥
git push               # 同步到远程仓库（已建立跟踪的分支直接 push）
```

习惯：**每完成一个小任务（一个文件/一个接口/一个页面）→ commit 一次**，每个 Phase 完成 → push + PR 合入 main。

---

## 六、当前仓库状态（Phase 1 结束时）

- 本地分支：`main`（第一次提交 + 文档补全提交）、`dev/szdjf`
- 远程分支：`main`、`dev/szdjf`（Public 公开）
- 默认分支：`main`
- 待办：Phase 1 文档文件尚未提交（本文档），按规范提交到 dev/szdjf → 下次 PR 带进 main
