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
    // 年龄分组
    const bins = [0, 18, 25, 35, 45, 60, 100]
    const labels = ['18岁以下', '18-24', '25-34', '35-44', '45-59', '60及以上']
    const ageGroup: Record<string, { total: number, count: number }> = {}
    users.forEach((u: any) => {
        const age = Number(u.age)
        let group = labels[labels.length - 1]
        for (let i = 0; i < bins.length - 1; i++) {
            if (age >= bins[i] && age < bins[i + 1]) {
                group = labels[i]
                break
            }
        }
        if (!ageGroup[group]) ageGroup[group] = { total: 0, count: 0 }
        ageGroup[group].total += userAmount[u.user_id] || 0
        ageGroup[group].count += 1
    })
    // 计算人均消费
    const data = labels.map(l => ({
        name: l,
        value: ageGroup[l] && ageGroup[l].count ? (ageGroup[l].total / ageGroup[l].count).toFixed(2) : 0
    }))
    option.value = {
        title: { text: '各年龄段人均消费能力', left: 'center' },
        tooltip: { trigger: 'axis' },
        xAxis: { type: 'category', data: labels },
        yAxis: { type: 'value' },
        series: [{ data: data.map(d => d.value), type: 'bar' }]
    }
})
</script>