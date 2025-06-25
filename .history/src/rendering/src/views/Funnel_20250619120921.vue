<template>
    <EchartsBase :option="option" height="400px" />
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import EchartsBase from '../components/EchartBase.vue'

const option = ref({})

type Step = '浏览' | '加购' | '下单'
const steps: Step[] = ['浏览', '加购', '下单']
const stepMap: Record<Step, Set<string>> = {
    '浏览': new Set(),
    '加购': new Set(),
    '下单': new Set()
}

onMounted(async () => {
    const res = await fetch('/user_logs.json')
    const data = await res.json()
    data.forEach((item: any) => {
        if (steps.includes(item.action) && item.user_id) {
            stepMap[item.action as Step].add(item.user_id)
        }
    })
    // 统计每一步的用户数
    const funnelData = steps.map(step => ({
        name: step,
        value: stepMap[step].size
    }))
    option.value = {
        title: { text: '转化漏斗', left: 'center' },
        tooltip: { trigger: 'item', formatter: '{b}: {c}' },
        series: [
            {
                name: '转化',
                type: 'funnel',
                left: '10%',
                width: '80%',
                label: { position: 'inside' },
                data: funnelData
            }
        ]
    }
})
</script>