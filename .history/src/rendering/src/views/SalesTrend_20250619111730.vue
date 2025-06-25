<template>
    <EchartsBase :option="option" height="400px" />
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
// @ts-ignore
import EchartsBase from '../components/EchartsBase.vue'

const option = ref({})

onMounted(async () => {
    const res = await fetch('/data/orders.json')
    const data = await res.json()
    // 统计每月销售额
    const monthly: Record<string, number> = {}
    data.forEach((item: any) => {
        if (!item.order_date || !item.amount) return
        const month = item.order_date.slice(0, 7)
        monthly[month] = (monthly[month] || 0) + Number(item.amount)
    })
    const months = Object.keys(monthly).sort()
    const sales = months.map(m => monthly[m])
    option.value = {
        title: { text: '月度销售趋势' },
        tooltip: { trigger: 'axis' },
        xAxis: { type: 'category', data: months },
        yAxis: { type: 'value' },
        series: [{ data: sales, type: 'line', areaStyle: {} }]
    }
})
</script>