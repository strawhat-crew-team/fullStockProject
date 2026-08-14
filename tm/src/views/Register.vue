<template>
  <div class="register-page">
    <el-card class="register-card">
      <h2 class="title">注册</h2>
      <el-form ref="formRef" :model="form" :rules="rules" label-width="60px">
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="form.phone" placeholder="请输入手机号" autocomplete="new-password"/>
        </el-form-item>
        <el-form-item label="昵称" prop="nickname">
          <el-input v-model="form.nickname" placeholder="请输入昵称" autocomplete="new-password"/>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" show-password autocomplete="new-password"/>
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input v-model="form.confirmPassword" type="password" placeholder="请再次输入密码" show-password autocomplete="new-password"/>
        </el-form-item>
        <el-button type="primary" :loading="loading" style="width:100%" @click="handleRegister">
          注 册
        </el-button>
        <p class="tip">已有账号?
          <router-link to="/login">去登录</router-link>
        </p>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import http from '../api/http.js'

const router = useRouter()
const formRef = ref(null)

const form = reactive({
  phone: '',
  nickname: '',
  password: '',
  confirmPassword: '',
})

const loading = ref(false)

const rules = {
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3456789]\d{9}$/, message: '手机号格式不对', trigger: 'blur' }
  ],
  nickname: [
    { required: true, message: '请输入昵称', trigger: 'blur' },
    { min: 1, max: 20, message: '昵称长度 1-20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度在6-20个字符之间', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    {
      // validator: 自定义校验函数. 前两个规则的 message/pattern 满足不了"两次密码一致"这种
      // 需要读其他字段的比对, 所以给这个字段挂一个函数, 校验时由组件调用
      validator: (rule, value, callback) => {
        // rule: 当前这条规则对象(这里用不上, 但参数是固定的, 必须占位)
        // value: 用户在这个输入框里填的值(确认密码)
        // callback: 校验结果的回执函数. 组件会等它:
        //   校验通过 → callback() 不传参
        //   校验失败 → callback(new Error('提示文字')), 组件把 Error 里的文字显示成红字
        if (value !== form.password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

async function handleRegister() {
  try{
    await formRef.value.validate()

    loading.value = true

    const data = await http.post('/register', {
      phone: form.phone,
      password: form.password,
      nickname: form.nickname
    })

    ElMessage.success('注册成功')

    router.push('/login')

  }catch(err) {
    ElMessage.error(err.response?.data?.detail || '注册失败')
  }finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-page {
  height: 100vh; /* 占满整个视口高度 */
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
  background: #f5f7fa;
}

.register-card {
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