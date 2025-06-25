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
import ProductRank from './views/ProductRank.vue'
import UserBehavior from './views/UserBehavior.vue'
import Funnel from './views/Funnel.vue'
import RFMScatter from './views/RFMScatter.vue'
import RFMRadar from './views/RFMRadar.vue'
import RFMBubble from './views/RFMBubble.vue'
import CategorySales from './views/CategorySales.vue'
import CategoryHeatmap from './views/CategoryHeatmap.vue'
import PaymentAnalysis from './views/PaymentAnalysis.vue'
import AgeConsumption from './views/AgeConsumption.vue'
import GenderConsumption from './views/GenderConsumption.vue'
import UserRetention from './views/UserRetention.vue'
import RegionConsumption from './views/RegionConsumption.vue'

const tabs = [
  { key: 'sales', label: '月度销售趋势', component: SalesTrend },
  { key: 'product', label: '产品销售排行', component: ProductRank },
  { key: 'behavior', label: '用户行为分布', component: UserBehavior },
  { key: 'funnel', label: '转化漏斗', component: Funnel },
  { key: 'rfm_scatter', label: '用户价值分群', component: RFMScatter },
  { key: 'rfm_radar', label: 'RFM集群雷达图', component: RFMRadar },
  { key: 'rfm_bubble', label: '客户价值分群气泡图', component: RFMBubble },
  { key: 'category_sales', label: '各品类销售情况', component: CategorySales },
  { key: 'category_heatmap', label: '品类关联热力图', component: CategoryHeatmap },
  { key: 'payment', label: '支付方式分析', component: PaymentAnalysis },
  { key: 'age', label: '各年龄段消费能力', component: AgeConsumption },
  { key: 'gender', label: '性别消费差异', component: GenderConsumption },
  { key: 'retention', label: '用户留存分析', component: UserRetention },
  { key: 'region', label: '地域消费分析', component: RegionConsumption }
]
const activeTab = ref(0)
</script>