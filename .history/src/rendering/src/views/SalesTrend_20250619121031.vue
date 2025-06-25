<template>
    <EchartBase :option="option" height="400px" />
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import EchartBase from '../components/EchartBase.vue'

const option = ref({})

function getMonth(dateStr: string) {
    return dateStr.slice(0, 7)
}

onMounted(async () => {
    try {
        const [ordersRes, orderItemsRes] = await Promise.all([
            fetch('/orders.json'),
            fetch('/order_items.json')
        ])
        if (!ordersRes.ok || !orderItemsRes.ok) throw new Error('数据文件未找到')
        const orders = await ordersRes.json()
        const orderItems = await orderItemsRes.json()
        // 计算每个订单金额
        const orderAmount: Record<string, number> = {}
        orderItems.forEach((item: any) => {
            orderAmount[item.order_id] = (orderAmount[item.order_id] || 0) + Number(item.price) * Number(item.quantity)
        })
        // 统计每月销售额
        const monthSales: Record<string, number> = {}
        orders.forEach((o: any) => {
            const m = getMonth(o.order_date)
            monthSales[m] = (monthSales[m] || 0) + (orderAmount[o.order_id] || 0)
        })
        const months = Object.keys(monthSales).sort()
        option.value = {
            title: { text: '月度销售趋势', left: 'center' },
            tooltip: { trigger: 'axis' },
            xAxis: { type: 'category', data: months },
            yAxis: { type: 'value' },
            series: [{ data: months.map(m => monthSales[m]), type: 'line', smooth: true }]
        }
    } catch (e) {
        console.error('月度销售趋势数据加载失败', e)
    }
})
</script>