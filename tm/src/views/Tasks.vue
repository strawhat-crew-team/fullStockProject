<template>
  <!-- ==================== 模板部分（页面长什么样） ==================== -->
  <div class="tasks-page">
    <!-- 顶部栏：标题 + 新建按钮 -->
    <div class="page-header">
      <h2>任务管理</h2>
      <!-- @click="openCreate"：事件连接线。点击按钮 → 执行 script 里的 openCreate 函数
           （不加括号 = 传函数本身，让事件系统到时候调用；加括号 = 立刻执行，那是错误的） -->
      <el-button type="primary" @click="openCreate">新建任务</el-button>
    </div>

    <!-- el-table：数据表格组件。
         :data="tasks"：属性连接线（带冒号=JS 表达式）。tasks 是 script 里的数组，表格自动渲染成行
         stripe：斑马纹（隔行变色），固定写法不用动 -->
    <el-table :data="tasks" stripe>
      <!-- el-table-column：一列。
           prop="code"：告诉这一列取每行对象的哪个字段
           label="编号"：列标题文字
           width/min-width：列宽（px），min-width 是"至少这么宽，空间多了自动撑开" -->
      <el-table-column prop="code" label="编号" width="100"/>
      <el-table-column prop="subject" label="主题" min-width="150"/>
      <el-table-column prop="sub_task" label="子任务" min-width="180"/>
      <el-table-column label="目标/计划工时" width="130">
        <!-- 作用域插槽：#default="scope" = "往这一列的洞里塞自定义内容，同时表格把当前行数据通过 scope 给我"
             scope.row = 当前这一行的数据对象（比如 {code:'TASK-001', target_hours:2, ...}）
             没有 prop 的列，显示内容完全由插槽决定 -->
        <template #default="scope">{{ scope.row.target_hours }} / {{ scope.row.plan_hours }}</template>
      </el-table-column>
      <el-table-column prop="date" label="日期" width="110"/>
      <el-table-column label="状态" width="90">
        <template #default="scope">
          <!-- el-tag：小标签组件。:type="..." 控制颜色（success 绿 / info 灰）
               is_archived 是后端返回的布尔字段：true=已归档，false=进行中
               {{ }}：模板里的表达式插值，把 JS 计算结果显示出来 -->
          <el-tag :type="scope.row.is_archived ? 'info' : 'success'">
            {{ scope.row.is_archived ? '已归档' : '进行中' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="230">
        <template #default="scope">
          <!-- 三个操作按钮，都拿到当前行数据 scope.row -->
          <el-button size="small" @click="openEdit(scope.row)">编辑</el-button>
          <!-- :disabled="scope.row.is_archived"：已归档的任务禁用归档按钮（再归档没意义）
               布尔值直接当属性传：true=按钮变灰不可点 -->
          <el-button size="small" :disabled="scope.row.is_archived" @click="handleArchive(scope.row)">归档</el-button>
          <!-- el-popconfirm：删除确认气泡。点"删除"先弹气泡问"确定吗"，点气泡里的"确定"才触发 @confirm
               #reference 插槽 = 往气泡里塞"触发按钮"（这是 Element Plus 规定的写法） -->
          <el-popconfirm title="确定删除这个任务吗？" @confirm="handleDelete(scope.row)">
            <template #reference>
              <el-button size="small" type="danger">删除</el-button>
            </template>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>

    <!-- el-dialog：弹窗组件。
         v-model="dialogVisible"：双向连接线。true=显示弹窗，false=关闭
         :title 属性：弹窗标题。isEdit 是 script 里的布尔：true 显示"编辑任务"，false 显示"新建任务"
         width：弹窗宽度。元素组件里布尔/数字/对象/变量都用冒号传，字符串字面量才不带冒号 -->
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑任务' : '新建任务'" width="560px">
      <!-- ref="formRef"：ref 连接线。模板里这个 el-form 实例会被塞进 script 的 formRef 变量
           （注意：formRef 必须叫这个名字，script 里 const formRef = ref(null) 同名才接得上）
           :model="form"：表单数据源，所有 el-form-item 的 v-model 都从 form 这个对象取字段
           :rules="rules"：校验规则。rules 是 script 里定义的对象，结构和 Login.vue 一样 -->
      <el-form ref="formRef" :model="form" :rules="rules" label-width="90px">
        <!-- label-width="90px"：左侧文字标签固定宽度，让所有输入框对齐 -->
        <el-form-item label="编号" prop="code">
          <!-- v-model="form.code"：双向连接线。输入框内容 ↔ form.code，任何一边变另一边跟着变 -->
          <el-input v-model="form.code" placeholder="如 TASK-001"/>
        </el-form-item>
        <el-form-item label="主题" prop="subject">
          <el-input v-model="form.subject" placeholder="这个任务要做什么"/>
        </el-form-item>
        <el-form-item label="子任务" prop="sub_task">
          <el-input v-model="form.sub_task" placeholder="拆成哪些小步骤"/>
        </el-form-item>
        <!-- el-input-number：数字输入框（自带加减按钮）。
             v-model 绑定数字；:min/:max 限制范围（冒号传数字 0 和 1000） -->
        <el-form-item label="目标工时" prop="target_hours">
          <el-input-number v-model="form.target_hours" :min="0" :max="1000"/>
        </el-form-item>
        <el-form-item label="计划工时" prop="plan_hours">
          <el-input-number v-model="form.plan_hours" :min="0" :max="1000"/>
        </el-form-item>
        <!-- el-date-picker：日期时间选择器。
             type="datetime"：精确到时分秒（对应后端 start_time 字段的 datetime 类型）
             value-format="YYYY-MM-DD HH:mm:ss"：v-model 拿到的必须是这个格式的字符串。
               不写它，组件给的是 Date 对象，JSON 序列化后变成 "2026-08-14T10:00:00" 这种
               带 T 的格式，后端 Pydantic 也能解析，但前后端格式约定统一字符串最稳 -->
        <el-form-item label="开始时间" prop="start_time">
          <el-date-picker v-model="form.start_time" type="datetime" value-format="YYYY-MM-DD HH:mm:ss" placeholder="选择开始时间"/>
        </el-form-item>
        <el-form-item label="结束时间" prop="end_time">
          <el-date-picker v-model="form.end_time" type="datetime" value-format="YYYY-MM-DD HH:mm:ss" placeholder="选择结束时间"/>
        </el-form-item>
        <!-- type="date"：只选日期不选时间（对应后端 date 字段，值格式 YYYY-MM-DD） -->
        <el-form-item label="日期" prop="date">
          <el-date-picker v-model="form.date" type="date" value-format="YYYY-MM-DD" placeholder="选择日期"/>
        </el-form-item>
        <el-form-item label="实际工时" prop="actual_hours">
          <el-input-number v-model="form.actual_hours" :min="0" :max="1000"/>
        </el-form-item>
      </el-form>
      <!-- #footer：el-dialog 规定的底部插槽，放按钮 -->
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <!-- :loading="submitting"：提交期间按钮转圈+禁用，防止连点（loading 变量控制） -->
        <el-button type="primary" :loading="submitting" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>


<script setup>
// ==================== 逻辑部分（页面怎么干活） ====================
import { ref, reactive, onMounted } from 'vue'
// ref：包一个值，取值用 .value（数字、布尔、数组都用它）
// reactive：包一个对象，直接 .属性（表单这种字段多的对象用它）
// onMounted：生命周期钩子。"页面挂载完成后"执行一次——进页面就自动加载任务列表

import http from '../api/http.js'
// http：axios 封装实例，登录页已经用过（baseURL=/api + 拦截器自动拼 token）

import { ElMessage } from 'element-plus'
// ElMessage：Element Plus 的消息提示函数（弹出顶部的小通知条）
// 注意：它是 JS 函数不是组件，不会因为 main.js 全局注册而自动可用，必须显式 import（Login 页同款）

// ---------- 数据 ----------
const formRef = ref(null)            // 拿到 el-form 组件实例（模板里 ref="formRef" 与这里同名绑定）
// 模板 ref="formRef" ↔ script const formRef = ref(null)：两条线对上，模板里的 el-form 实例才能用
// formRef.value = 组件实例本身，.validate() 是它提供的校验方法
const tasks = ref([])            // 任务列表数组。表格 :data="tasks" 读的就是它
const dialogVisible = ref(false) // 弹窗开关。true=弹窗显示
const isEdit = ref(false)        // 当前是编辑(true)还是新建(false)，决定标题和调哪个接口
const submitting = ref(false)    // 提交中标志。true=确定按钮转圈
const editingId = ref(null)      // 正在编辑的任务 id（后端 PUT 路径里要带它；新建时是 null）

// 表单数据源：字段名必须和后端 TaskCreate/TaskResponse 完全一致（联调第一原则）
const form = reactive({
  code: '',            // 编号
  subject: '',         // 主题
  sub_task: '',        // 子任务
  target_hours: 0,     // 目标工时（数字）
  plan_hours: 0,       // 计划工时
  start_time: '',      // 开始时间（字符串，值格式由 el-date-picker 的 value-format 保证）
  end_time: '',        // 结束时间
  date: '',            // 日期
  actual_hours: 0,     // 实际工时
})

// 校验规则：required 必填 + 触发时机 blur（失焦时校验）
// 注意：提交时调 validate() 会无条件检查全部规则，不受 trigger 限制（Login 页讲过）
const rules = {
  code: [{ required: true, message: '请输入任务编号', trigger: 'blur' }],
  subject: [{ required: true, message: '请输入任务主题', trigger: 'blur' }],
}

// ---------- 方法 ----------
// 加载任务列表：进页面(onMounted)和每次增删改成功后都调用
async function loadTasks() {
  // http.get('/tasks') 返回的就是任务数组本身！
  // 原因：http.js 的响应拦截器已经 return response.data（剥掉 axios 响应外壳），
  // 所以这里不能再写 .data——数组.data = undefined，表格会一直空白（联调踩过的坑）
  tasks.value = await http.get('/tasks')
}

// 点"新建任务"：清空表单 + 切换成新建模式 + 打开弹窗
function openCreate() {
  isEdit.value = false          // 标记成"新建"
  editingId.value = null        // 没有编辑对象
  // Object.assign(目标对象, 源对象)：把源对象的字段逐个拷进目标对象
  // 这里的效果 = 把 form 重置成初始值（新建时表单必须干净）
  Object.assign(form, { code: '', subject: '', sub_task: '', target_hours: 0, plan_hours: 0, start_time: '', end_time: '', date: '', actual_hours: 0 })
  dialogVisible.value = true    // 打开弹窗
}

// 点"编辑"：把这一行的数据填进表单 + 切换成编辑模式 + 打开弹窗
function openEdit(row) {
  isEdit.value = true                      // 标记成"编辑"
  editingId.value = row.id                 // 记住这个任务的 id（提交时用）
  // 行数据 → 表单。注意日期字段要"翻译"：
  // 后端返回的 start_time 是 ISO 格式 "2026-08-14T10:00:00"（带 T），
  // 而日期选择器要求 "2026-08-14 10:00:00"（空格分隔）。replace('T',' ') 换成空格，再截前 19 位
  // （不处理的话，日期选择器显示不出已选值——格式对不上）
  Object.assign(form, {
    code: row.code,
    subject: row.subject,
    sub_task: row.sub_task,
    target_hours: row.target_hours,
    plan_hours: row.plan_hours,
    start_time: row.start_time ? row.start_time.replace('T', ' ').slice(0, 19) : '',
    end_time: row.end_time ? row.end_time.replace('T', ' ').slice(0, 19) : '',
    date: row.date ? row.date.slice(0, 10) : '',
    actual_hours: row.actual_hours,
  })
  dialogVisible.value = true               // 打开弹窗
}

// 点"确定"：先校验，再按模式调 POST(新建) 或 PUT(编辑)
async function handleSubmit() {
  submitting.value = true         // 按钮转圈（防止连点）
  try {
    await formRef.value.validate()  // 先过校验（编号/主题必填）；不过会抛异常，被 catch 接住
    // 提交前处理日期字段：el-date-picker 没选时给的是空字符串 ''，而后端日期字段是 datetime 类型，
    // 收到 '' 解析不成时间 → 422。必须把空串转成 null（null 才等于"不传"）
    const payload = {
      ...form,                              // 展开 form 的全部字段
      start_time: form.start_time || null,  // 空串 → null；有值（"2026-08-14 10:00:00"）就原样传
      end_time: form.end_time || null,
      date: form.date || null,
    }
    if (isEdit.value) {
      // 编辑：PUT /api/tasks/{id}，body 只发表单字段（id 在路径里，不需要发给后端）
      await http.put(`/tasks/${editingId.value}`, payload)
      ElMessage.success('任务已更新')
    } else {
      // 新建：POST /api/tasks，后端返回 201 + 新任务对象
      await http.post('/tasks', payload)
      ElMessage.success('任务创建成功')
    }
    dialogVisible.value = false  // 成功 → 关弹窗
    loadTasks()                  // 刷新列表（新数据从后端重新拉一遍）
  } catch (err) {
    // 校验失败或请求失败都走到这里。校验失败时 el-form 已自动渲染红字提示，这里给个兜底
    ElMessage.error(err.response?.data?.detail || '保存失败')
  } finally {
    submitting.value = false     // 无论成败，结束转圈
  }
}

// 归档：把任务标记为已完成（后端把 is_archived 置 true）
async function handleArchive(row) {
  await http.post(`/tasks/${row.id}/archive`)  // POST /api/tasks/{id}/archive
  ElMessage.success('已归档')
  loadTasks()                                   // 刷新列表（状态列会变灰）
}

// 删除：气泡确认后触发。删的是自己列表里的任务，后端按 user_id 校验所有权
async function handleDelete(row) {
  await http.delete(`/tasks/${row.id}`)  // DELETE /api/tasks/{id} → 后端 204 无内容
  ElMessage.success('已删除')
  loadTasks()                            // 刷新列表
}

// 页面挂载完成 → 自动加载任务列表（生命周期钩子，只执行一次）
onMounted(() => {
  loadTasks()
})
</script>


<style scoped>
/* scoped：样式只作用于本页面的元素，不影响其他页面（Vue 会给本页元素加特殊属性做隔离） */
.tasks-page {
  padding: 20px;
}
.page-header {
  display: flex;           /* 弹性布局：两个子元素排一行 */
  justify-content: space-between; /* 左右两端对齐（标题在左，按钮在右） */
  align-items: center;     /* 垂直居中 */
  margin-bottom: 16px;
}
</style>
