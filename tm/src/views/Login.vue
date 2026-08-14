<template>
  <div class="login-page">
    <el-card class="login-card">
      <h2 class="title">登录</h2>
      <el-form ref="formRef" :model="form" :rules="rules" label-width="60px">
        <el-form-item label="手机号" prop="phone">
          <!-- autocomplete="new-password": 告诉浏览器"这是创建新密码的输入框", 阻止它自动填充已保存的账号密码.
               Element Plus 会把该属性透传到原生 input 上. 注意不能写 autocomplete="username", 那会主动邀请浏览器填充 -->
          <el-input v-model="form.phone" placeholder="请输入手机号" autocomplete="new-password"/>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" show-password autocomplete="new-password"/>
        </el-form-item>
        <el-button type="primary" :loading="loading" style="width:100%" @click="handleLogin">
          登 录
        </el-button>
        <p class="tip">还没有账号?
          <router-link to="/register">去注册</router-link>
        </p>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import {ref, reactive} from 'vue'
import {useRouter} from 'vue-router'
import {ElMessage} from 'element-plus'
import http from '../api/http.js'

const router = useRouter()
const formRef = ref(null)

// 表单数据 v-model双向绑定， 用户输入什么这里就有什么
const form = reactive({
  phone: '',
  password: '',
})

const loading = ref(false)

const rules = {
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3456789]\d{9}$/, message: '手机号格式不对', trigger: 'blur'}
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    {min: 6, max: 20, message: '密码长度在6-20个字符之间', trigger: 'blur'}
  ]
}

async function handleLogin() {
  try {
    await formRef.value.validate()

    loading.value = true

    const data = await http.post('/login', {
      phone: form.phone,
      password: form.password
    })

    localStorage.setItem('token', data.access_token)

    router.push('/tasks')

    ElMessage.success('登录成功')
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '登录失败')
  } finally {
    loading.value = false
  }
}



</script>

<style scoped>
.login-page {
  height: 100vh; /* 占满整个视口高度 */
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
  background: #f5f7fa;
}

.login-card {
  width: 400px;
  padding: 20px;
}

.title {
  text-align: center;
  margin-bottom: 20px;
}

.tip {
  text-align: center;
  margin-top: 12px;
  font-size: 14px;
  color: #666;
}
</style>