<template>
  <!-- ==================== 模板部分（页面长什么样） ==================== -->
  <!-- Dashboard 页面 = 数据概览首页，展示统计卡片 + 两个图表
       布局：标题 → 一行三张统计卡片 → 一行两个图表（折线图 + 环形图） -->
  <div class="dashboard-page">
    <h2>数据概览</h2>

    <!-- 统计卡片区：三张卡片一行 -->
    <div class="cards">
      <!-- 卡片1：总任务数。{{ }} 插值 = 把 JS 变量的值渲染到页面上 -->
      <div class="card">
        <div class="card-label">总任务数</div>
        <div class="card-value">{{ stats.total }}</div>
      </div>
      <!-- 卡片2：已完成数 -->
      <div class="card">
        <div class="card-label">已完成</div>
        <div class="card-value">{{ stats.done }}</div>
      </div>
      <!-- 卡片3：完成率。rateText 是 JS 里的计算属性（负责把 0.12 变成 "12%" 的字符串） -->
      <div class="card">
        <div class="card-label">完成率</div>
        <div class="card-value">{{ rateText }}</div>
      </div>
    </div>

    <!-- 图表区：两个图表容器并排。
         ref="dailyChartRef"：ref 连接线——这个 div 的 DOM 元素会塞进 script 的 dailyChartRef 变量
         echarts 需要一个 DOM 元素作为画布挂载点，init(元素) 就在这个 div 里渲染图表
         注意：容器必须设宽高（下面的 CSS），否则 echarts 不知道画多大 -->
    <div class="charts">
      <div ref="dailyChartRef" class="chart-box"></div>
      <div ref="rateChartRef" class="chart-box"></div>
    </div>
  </div>
</template>


<script setup>
// ==================== 逻辑部分（页面怎么干活） ====================
// 数据流：进页面 → 拉两个统计接口 → 填卡片数据 → 把数据组装成图表配置 → echarts 画图
import { ref, reactive, computed, onMounted, onBeforeUnmount } from 'vue'
// 新面孔 onBeforeUnmount：生命周期钩子，"组件即将销毁时"执行——图表实例在这里释放（防内存泄漏）

import http from '../api/http.js'
// http：axios 封装（拦截器已剥一层，返回值直接是后端 body）

import * as echarts from 'echarts'
// echarts：图表库（npm install 装的）。* as = 把整个库的所有导出打包成 echarts 对象
// 用法三步：init(容器DOM) 创建实例 → setOption(配置) 画图 → dispose() 销毁

// ---------- 数据 ----------
// 统计卡片数据（模板里 {{ stats.total }} / {{ stats.done }} / {{ rateText }} 读的就是它）
const stats = reactive({
  total: 0,  // 总任务数
  done: 0,   // 已完成数
  rate: 0,   // 完成率（小数 0.12）
})

// 计算属性：rate(0~1 小数) → "12%" 显示文本
// computed 的规则：函数里用到的响应式数据变了，返回值自动重新计算
// toFixed(0) = 保留 0 位小数；rate=0.125 时 → 12.5 → toFixed(0) → "13"? 不，toFixed 四舍五入
// 注意：12.5 的 toFixed(0) 在 JS 里是 "13"(银行家舍入有例外)，这里 rate=0.12 显示 12%，够用
const rateText = computed(() => (stats.rate * 100).toFixed(0) + '%')

// 图表容器（模板 ref="dailyChartRef" / ref="rateChartRef" 与这里同名绑定）
const dailyChartRef = ref(null)  // 折线图挂载点
const rateChartRef = ref(null)   // 环形图挂载点

// 图表实例：存普通变量就行（不需要响应式——图表是 DOM 世界的，不参与 Vue 的响应式渲染）
let dailyChart = null
let rateChart = null

// ---------- 方法 ----------
// 加载数据 + 画图（onMounted 触发）
async function loadDashboard() {
  // 1. 拉数据（两个接口并行发，await Promise.all 等两个都回来）
  // Promise.all([p1, p2])：两个请求同时发，返回 [结果1, 结果2]
  const [daily, eff] = await Promise.all([
    http.get('/stats/daily'),       // 数组：[{date, hours}, ...]
    http.get('/stats/efficiency'),  // 对象：{total, done, rate}
  ])

  // 2. 填卡片数据（模板自动刷新显示）
  stats.total = eff.total
  stats.done = eff.done
  stats.rate = eff.rate

  // 3. 画折线图（每日工时）
  // .map(d => d.date)：把数组每个对象"映射"成它的 date 字段 → ["2026-08-14", ...]
  dailyChart = echarts.init(dailyChartRef.value)  // init(容器DOM元素) → 创建图表实例
  dailyChart.setOption({
    title: { text: '每日工时' },            // 图表左上角标题
    tooltip: { trigger: 'axis' },          // 鼠标悬停提示；axis = 以"坐标轴"为单位整列提示（折线图惯例）
    xAxis: {                               // 横轴（类别轴）
      type: 'category',                    // category = 类别轴（日期/名字这种离散值）
      data: daily.map((d) => d.date),      // 横轴数据：所有日期
    },
    yAxis: {                               // 纵轴（数值轴）
      type: 'value',                       // value = 数值轴（数字大小）
      name: '小时',                         // 轴的单位标注
    },
    series: [{                             // 系列：真正画出来的图形
      type: 'line',                        // 折线图
      data: daily.map((d) => d.hours),     // 每个日期的工时 → 每个点的纵坐标
      smooth: true,                        // 曲线平滑（直线变波浪线）
    }],
  })

  // 4. 画环形图（完成率）
  rateChart = echarts.init(rateChartRef.value)
  rateChart.setOption({
    title: { text: '完成率' },
    tooltip: { trigger: 'item' },          // item = 悬停到哪块显示哪块（饼图惯例）
    series: [{
      type: 'pie',                         // 饼图
      radius: ['40%', '70%'],              // 内径40% 外径70% → 中间挖空 = 环形（甜甜圈）
      data: [                              // 每一块：名字 + 数值（数值占比决定扇形大小）
        { name: '已完成', value: eff.done },            // 已完成块
        { name: '未完成', value: eff.total - eff.done } // 未完成块（总数 - 已完成）
      ],
    }],
  })
}

// 页面挂载完成 → 加载数据画图（容器 DOM 此刻已渲染，ref 可用）
onMounted(() => {
  loadDashboard()
})

// 组件即将销毁（切到别的页面）→ 释放图表实例
// 为什么必须释放：echarts 实例内部会持续监听窗口/事件，不销毁就常驻内存 → 页面切多了内存泄漏（越切越卡）
onBeforeUnmount(() => {
  if (dailyChart) dailyChart.dispose()  // dispose() = 销毁实例，释放它占的资源
  if (rateChart) rateChart.dispose()
})
</script>


<style scoped>
/* scoped：样式只作用于本页面元素，不影响其他页面 */
.dashboard-page {
  padding: 20px;
}

/* 卡片区：flex 弹性布局，三张卡片横排，卡片之间留间隙 */
.cards {
  display: flex;
  gap: 16px;            /* 子元素间距 16px */
  margin-bottom: 20px;  /* 与下方图表区拉开距离 */
}

/* 每张卡片：白底圆角 + 细边框，居中显示 */
.card {
  flex: 1;              /* 三张卡片等分宽度 */
  background: #fff;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  padding: 20px;
  text-align: center;   /* 文字居中 */
}

/* 卡片标题：小号灰色字 */
.card-label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}

/* 卡片数值：大号加粗主色 */
.card-value {
  font-size: 28px;
  font-weight: bold;
  color: #409eff;
}

/* 图表区：两个图表横排，间距 16px */
.charts {
  display: flex;
  gap: 16px;
}

/* 每个图表容器：等分宽度 + 固定高度（echarts 需要确定尺寸） */
.chart-box {
  flex: 1;
  height: 360px;
  background: #fff;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
}
</style>
