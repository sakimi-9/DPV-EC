<template>
    <EchartBase :option="option" height="400px" />
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import EchartBase from '../components/EchartBase.vue'

const option = ref({})

onMounted(async () => {
    const [usersRes, ordersRes, orderItemsRes] = await Promise.all([
        fetch('/users.json'),
        fetch('/orders.json'),
        fetch('/order_items.json')
    ])
    const users = await usersRes.json()
    const orders = await ordersRes.json()
    const orderItems = await orderItemsRes.json()
    // 计算每个订单金额
    const orderAmount: Record<string, number> = {}
    orderItems.forEach((item: any) => {
        orderAmount[item.order_id] = (orderAmount[item.order_id] || 0) + Number(item.price) * Number(item.quantity)
    })
    // 计算每个用户总消费
    const userAmount: Record<string, number> = {}
    orders.forEach((o: any) => {
        if (!o.user_id) return
        userAmount[o.user_id] = (userAmount[o.user_id] || 0) + (orderAmount[o.order_id] || 0)
    })
    // 城市消费
    const cityMap: Record<string, number> = {}
    users.forEach((u: any) => {
        if (!u.city) return
        cityMap[u.city] = (cityMap[u.city] || 0) + (userAmount[u.user_id] || 0)
    })
    // 取TOP10城市
    const topCities = Object.entries(cityMap).sort((a, b) => b[1] - a[1]).slice(0, 10)
    option.value = {
        title: { text: 'TOP10城市消费额', left: 'center' },
        tooltip: { trigger: 'axis' },
        xAxis: { type: 'category', data: topCities.map(c => c[0]), axisLabel: { rotate: 0 } },
        yAxis: { type: 'value' },
        series: [{ data: topCities.map(c => c[1]), type: 'bar' }]
    }
})
</script>