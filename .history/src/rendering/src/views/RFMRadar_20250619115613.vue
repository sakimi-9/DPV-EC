<template>
    <EchartBase :option="option" height="400px" />
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import EchartBase from '../components/EchartBase.vue'

const option = ref({})

onMounted(async () => {
    const res = await fetch('/rfm_radar.json')
    const data = await res.json()
    const indicators = [
        { name: 'Recency', max: 2, min: -2 },
        { name: 'Frequency', max: 2, min: -2 },
        { name: 'Monetary', max: 2, min: -2 }
    ]
    option.value = {
        title: { text: 'RFM各集群特征雷达图', left: 'center' },
        tooltip: {},
        legend: { data: data.map((d: any) => `集群${d.cluster + 1}`), top: 30 },
        radar: { indicator: indicators },
        series: [{
            type: 'radar',
            data: data.map((d: any) => ({
                value: [d.recency, d.frequency, d.monetary],
                name: `集群${d.cluster + 1}`
            }))
        }]
    }
})
</script>