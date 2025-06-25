<template>
    <EchartsBase :option="option" height="400px" />
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import EchartsBase from '../components/EchartBase.vue'

const option = ref({})

const actionMap = {
    'add_to_cart': '加购',
    'view': '浏览',
    'click': '点击',
    'purchase': '下单',
    'search': '搜索'
}

onMounted(async () => {
    const res = await fetch('/user_logs.json')
    const data = await res.json()
    // 统计各行为类型数量
    const actionCount: Record<string, number> = {}
    data.forEach((item: any) => {
        if (!item.action) return
        actionCount[item.action] = (actionCount[item.action] || 0) + 1
    })
    const actions = Object.keys(actionMap)
    option.value = {
        title: { text: '用户行为分布', left: 'center' },
        tooltip: { trigger: 'item' },
        legend: { orient: 'vertical', left: 'left', data: actions.map(a => actionMap[a]) },
        series: [
            {
                name: '行为类型',
                type: 'pie',
                radius: ['50%', '70%'],
                avoidLabelOverlap: false,
                label: { show: true, position: 'center', formatter: '{b}\n{d}%' },
                emphasis: { label: { show: true, fontSize: 20, fontWeight: 'bold' } },
                data: actions.map(a => ({ name: actionMap[a], value: actionCount[a] || 0 }))
            }
        ]
    }
})
</script>