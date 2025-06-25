<template>
    <EchartsBase :option="option" height="400px" />
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import EchartsBase from '../components/EchartBase.vue'

const option = ref({})

onMounted(async () => {
    const res = await fetch('/data/user_logs.json')
    const data = await res.json()
    // 统计各行为类型数量
    const actionMap: Record<string, number> = {}
    data.forEach((item: any) => {
        if (!item.action) return
        actionMap[item.action] = (actionMap[item.action] || 0) + 1
    })
    const actions = Object.keys(actionMap)
    option.value = {
        title: { text: '用户行为分布', left: 'center' },
        tooltip: { trigger: 'item' },
        legend: { orient: 'vertical', left: 'left' },
        series: [
            {
                name: '行为类型',
                type: 'pie',
                radius: ['50%', '70%'],
                avoidLabelOverlap: false,
                label: { show: true, position: 'center', formatter: '{b}\n{d}%' },
                emphasis: { label: { show: true, fontSize: 20, fontWeight: 'bold' } },
                data: actions.map(a => ({ name: a, value: actionMap[a] }))
            }
        ]
    }
})
</script>