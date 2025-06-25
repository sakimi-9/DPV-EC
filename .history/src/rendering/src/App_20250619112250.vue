<template>
  <div style="padding: 24px;">
    <h1 style="text-align:center; margin-bottom: 32px;">电商项目可视化</h1>
    <div style="display: flex; justify-content: center; gap: 16px; margin-bottom: 32px;">
      <button v-for="(tab, idx) in tabs" :key="tab.key" :style="{
        padding: '12px 24px',
        border: idx === activeTab ? '2px solid #409EFF' : '2px solid #eee',
        borderRadius: '8px',
        background: idx === activeTab ? '#e6f7ff' : '#fff',
        color: idx === activeTab ? '#409EFF' : '#333',
        fontWeight: 'bold',
        cursor: 'pointer'
      }" @click="activeTab = idx">
        {{ tab.label }}
      </button>
    </div>
    <component :is="tabs[activeTab].component" />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import SalesTrend from './views/SalesTrend.vue'
// 你后续可以继续引入其他图表组件

const tabs = [
  { key: 'sales', label: '月度销售趋势', component: SalesTrend },
  // 继续添加其他图表
]
const activeTab = ref(0)
</script>