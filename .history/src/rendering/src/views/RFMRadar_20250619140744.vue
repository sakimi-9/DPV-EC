<template>
    <div>
        <EchartBase :option="option" height="400px" />
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import EchartBase from '../components/EchartBase.vue'

const option = ref({})

onMounted(async () => {
    const res = await fetch('/rfm_radar.json')
    const data = await res.json()
    const indicators = [
        { name: '最近一次消费', max: 2, min: -2 },
        { name: '消费频率', max: 2, min: -2 },
        { name: '消费金额', max: 2, min: -2 }
    ]
    option.value = {
        title: { text: 'RFM各集群特征雷达图', left: 'center', top: 10 },
        tooltip: {},
        legend: { data: data.map((d: any) => `集群${d.cluster + 1}`), top: 40 },
        radar: {
            indicator: indicators,
            center: ['50%', '72%'], // 下移
            radius: 180 // 缩小半径
        },
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