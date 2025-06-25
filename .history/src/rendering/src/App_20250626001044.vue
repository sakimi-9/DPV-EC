<template>
  <div style="padding: 24px; position: relative; min-height: 100vh;">
    <h1 style="text-align:center; margin-bottom: 32px;">电商项目可视化</h1>
    <!-- 右侧显示数据分析开关，顶部与tab栏对齐 -->
    <div style="position: absolute; top: 90px; right: 40px; z-index: 10; display: flex; align-items: center; gap: 8px;">
      <span style="font-size: 16px;">显示数据分析</span>
      <button @click="showAnalysis = !showAnalysis" :style="{
        width: '48px', height: '24px', borderRadius: '12px', border: '2px solid #409EFF', background: showAnalysis ? '#409EFF' : '#fff', position: 'relative', cursor: 'pointer', transition: 'background 0.2s', padding: 0
      }">
        <span :style="{
          display: 'block', width: '20px', height: '20px', borderRadius: '50%', background: '#fff', position: 'absolute', top: '1px', left: showAnalysis ? '25px' : '3px', boxShadow: '0 1px 4px #888', transition: 'left 0.2s'
        }"></span>
      </button>
    </div>
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
    <!-- 黑框数据分析文本 -->
    <div v-if="showAnalysis && analysisText[tabs[activeTab].key]"
      style="margin: 32px auto 0; max-width: 900px; background: #eaf6ff; color: #222; border-radius: 12px; border: 2px solid #222; padding: 24px 32px; font-size: 18px; font-family: 'Microsoft YaHei', sans-serif; box-shadow: 0 2px 12px #0002; text-align: left;">
      <div v-html="analysisText[tabs[activeTab].key]" />
    </div>
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
const showAnalysis = ref(false)

// 分析文本内容
const analysisText: Record<string, string> = {
  sales: `<b>结论：</b>2022 年 2 月销售低谷，3 月回升，全年整体销售相对平稳。<br><b>建议：</b>2 月（春节前后）推出"春节不打烊"活动，保障供应与服务；3 月延续营销热度，用春季节日（如女神节）活动巩固增长；日常关注销售平稳期的用户需求，用主题活动（如每月会员日）拉动消费。`,
  product: `<b>结论：</b>母婴用品、电子产品在前 20 销售排行中占比高，是核心畅销品类。<br><b>建议：</b>扩充核心品类 SKU（如母婴新系列、电子产品升级款）；围绕这些品类打造"爆款专区"，搭配营销活动。`,
  behavior: `<b>结论：</b>浏览行为占主导，下单行为占比低，需提升转化效率。<br><b>建议：</b>通过优质内容（如测评、场景化展示）优化浏览体验；设置浏览后弹窗优惠、下单返现等活动，刺激下单转化。`,
  funnel: `<b>结论：</b>从浏览到加购、加购到下单均有流失，下单环节是关键转化卡点。<br><b>建议：</b>优化商品详情页（如突出卖点、简化信息）降低浏览-加购流失；加购后推送限时优惠、库存提醒，推动下单。`,
  rfm_scatter: `<b>结论：</b>集群 3 分布广但价值待挖掘，集群 1 集中体现高价值特征。<br><b>建议：</b>对集群 3 进行分层运营，筛选有潜力客群推送定制化优惠；集群 1 持续维护，深化高价值互动。`,
  rfm_bubble: `<b>结论：</b>消费频率、金额与最近消费存在关联，部分客群消费频率高但金额低，需挖掘潜力。<br><b>建议：</b>高频低额客群，推荐高性价比组合商品；低频高额客群，用专属服务、限量商品提升粘性。`,
  rfm_radar: `<b>结论：</b>集群 1 最近消费、消费金额、频率均优（高价值客群）；集群 3 消费频率、金额弱（需唤醒客群）。<br><b>建议：</b>集群 1 提供专属权益（如 VIP 服务、高端新品优先购）；集群 3 推送优惠券、爆款活动，刺激复购。`,
  category_sales: `<b>结论：</b>电子产品销售额领先，图书、母婴用品等品类销售额相对低。<br><b>建议：</b>加大电子产品推广，拓展高端、潮流品类；针对低销售额品类，挖掘细分爆款（如儿童图书礼盒、母婴刚需品组合）。`,
  category_heatmap: `<b>结论：</b>食品与多品类关联度高，电子产品、运动户外等品类间也存在较强消费关联。<br><b>建议：</b>基于关联度做组合营销（如食品+家居用品套餐）；在关联品类页面做交叉推荐，提升客单价。`,
  payment: `<b>结论：</b>支付宝、微信为主要支付方式，银行卡、花呗占比相对低。<br><b>建议：</b>保障主流支付渠道流畅；针对银行卡、花呗用户，推出支付满减、分期免息活动，引导使用。`,
  age: `<b>结论：</b>18 岁以下消费能力低，18 岁及以上各年龄段消费能力相对均衡。<br><b>建议：</b>针对 18 岁以下群体推出低客单价专属商品/套餐；18 岁及以上群体，依据品类偏好做精准营销。`,
  gender: `<b>结论：</b>男性与女性人均消费金额相近，性别对人均消费影响小。<br><b>建议：</b>无需针对性别差异调整定价，可统一聚焦品类、营销活动吸引消费。`,
  retention: `<b>结论：</b>2022 年 7-12 月新用户首月留存高，次月起留存波动下降，9 月新用户后期留存下滑更明显。<br><b>建议：</b>首月通过福利、优质服务强化体验；次月起用个性化推荐、专属活动（如老客回流券）提升留存；重点优化 9 月新用户留存策略，分析流失原因。`,
  region: `<b>结论：</b>成都、武汉等城市消费额高，北京、深圳相对靠后但仍具规模。<br><b>建议：</b>在高消费额城市办线下快闪、城市专属活动；针对北京、深圳，结合当地消费偏好（如高端、科技类商品）做营销。`
}

function exportAnalysisImage() {
  // 预留导出图片逻辑，后续补充
  alert('导出功能待补充图片后实现')
}
</script>