<template>
    <EchartBase :option="option" height="400px" />
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import EchartBase from '../components/EchartBase.vue'

const option = ref({})

onMounted(async () => {
    const res = await fetch('/orders.json')
    const orders = await res.json()
    // 统计每种支付方式的订单数
    const payMap: Record<string, number> = {}
    orders.forEach((o: any) => {
        if (!o.payment_method) return
        payMap[o.payment_method] = (payMap[o.payment_method] || 0) + 1
    })
    const pays = Object.keys(payMap)
    option.value = {
        title: { text: '支付方式分布', left: 'center' },
        tooltip: { trigger: 'item' },
        legend: { orient: 'vertical', left: 'left' },
        series: [{
            name: '支付方式',
            type: 'pie',
            radius: ['50%', '70%'],
            data: pays.map(p => ({ name: p, value: payMap[p] }))
        }]
    }
})
</script>