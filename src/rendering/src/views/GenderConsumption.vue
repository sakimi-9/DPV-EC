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
    // 性别分组
    const genderMap: Record<string, { total: number, count: number }> = {}
    users.forEach((u: any) => {
        const g = u.gender === 'F' ? '女性' : u.gender === 'M' ? '男性' : '未知'
        if (!genderMap[g]) genderMap[g] = { total: 0, count: 0 }
        genderMap[g].total += userAmount[u.user_id] || 0
        genderMap[g].count += 1
    })
    const genders = ['男性', '女性']
    const data = genders.map(g => ({
        name: g,
        value: genderMap[g] && genderMap[g].count ? (genderMap[g].total / genderMap[g].count).toFixed(2) : 0
    }))
    option.value = {
        title: { text: '性别人均消费对比', left: 'center' },
        tooltip: { trigger: 'axis' },
        xAxis: { type: 'category', data: genders },
        yAxis: { type: 'value' },
        series: [{ data: data.map(d => d.value), type: 'bar' }]
    }
})
</script>