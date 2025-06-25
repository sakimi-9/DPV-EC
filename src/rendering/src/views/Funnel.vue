<template>
    <EchartsBase :option="option" height="400px" />
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import EchartsBase from '../components/EchartBase.vue'

const option = ref({})

const actionMap = {
    'view': '浏览',
    'add_to_cart': '加购',
    'purchase': '下单'
}
const steps = ['view', 'add_to_cart', 'purchase']
const stepMap: Record<string, Set<string>> = { 'view': new Set(), 'add_to_cart': new Set(), 'purchase': new Set() }

onMounted(async () => {
    const res = await fetch('/user_logs.json')
    const data = await res.json()
    data.forEach((item: any) => {
        if (steps.includes(item.action) && item.user_id) {
            stepMap[item.action].add(item.user_id)
        }
    })
    const funnelData = steps.map(step => ({
        name: actionMap[step],
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