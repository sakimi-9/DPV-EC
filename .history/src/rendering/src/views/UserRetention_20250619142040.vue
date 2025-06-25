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
    const res = await fetch('/orders.json')
    const orders = await res.json()
    // 计算每个用户的首次购买月
    const userFirstMonth: Record<string, string> = {}
    orders.forEach((o: any) => {
        const m = getMonth(o.order_date)
        if (!userFirstMonth[o.user_id] || userFirstMonth[o.user_id] > m) {
            userFirstMonth[o.user_id] = m
        }
    })
    // 统计每月新用户
    const months = Array.from<string>(new Set(orders.map((o: any) => getMonth(o.order_date)))).sort()
    const cohort: Record<string, Set<string>> = {}
    months.forEach(m => { cohort[m] = new Set() })
    orders.forEach((o: any) => {
        const m = getMonth(o.order_date)
        cohort[m].add(o.user_id)
    })
    // 计算留存率
    const retention: Record<string, number[]> = {}
    months.forEach((m, i) => {
        const newUsers = Object.entries(userFirstMonth).filter(([_, fm]) => fm === m).map(([uid]) => uid)
        retention[m] = []
        for (let j = 0; j < 6; j++) {
            const nextMonth = months[i + j]
            if (!nextMonth) break
            const retained = orders.filter((o: any) => getMonth(o.order_date) === nextMonth && newUsers.includes(o.user_id))
            retention[m].push(newUsers.length ? (retained.length / newUsers.length * 100) : 0)
        }
    })
    // 取近6个月的留存
    const showMonths = months.slice(-6)
    option.value = {
        title: { text: '用户留存分析', left: 'center', top: 0 },
        tooltip: { trigger: 'axis' },
        legend: { data: showMonths.map(m => `${m}新用户`), top: 10 }, // 下移图例
        xAxis: { type: 'category', data: ['第1月', '第2月', '第3月', '第4月', '第5月', '第6月'] },
        yAxis: {
            type: 'value',
            axisLabel: { formatter: '{value}%' },
            max: 100
        },
        series: showMonths.map(m => ({
            name: `${m}新用户`,
            type: 'line',
            data: retention[m].map((v, i) => i === 0 ? 100 : Number(v.toFixed(2)))
        }))
    }
})
</script>