<template>
    <EchartBase :option="option" width="1000px" height="600px" />
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import EchartBase from '../components/EchartBase.vue'

const option = ref({})

const clusterColors = ['#5470C6', '#91CC75', '#FAC858', '#EE6666', '#73C0DE', '#3BA272']

onMounted(async () => {
    const res = await fetch('/rfm_bubble.json')
    const data = await res.json()
    option.value = {
        title: { text: '客户价值分群气泡图', left: 'center' },
        tooltip: {
            trigger: 'item',
            formatter: (p: any) =>
                `最近一次消费: ${p.value[0]}<br/>消费频率: ${p.value[1]}<br/>消费金额: ${p.value[2]}<br/>集群: ${p.value[3] + 1}`
        },
        legend: { data: Array.from(new Set(data.map((d: any) => `集群${d.cluster + 1}`))), top: 30 },
        grid: { left: 80, right: 40, top: 80, bottom: 60 }, // 加大内边距
        xAxis: { name: '最近一次消费' },
        yAxis: { name: '消费频率' },
        series: [{
            type: 'scatter',
            symbolSize: (val: any) => Math.log(val[2] + 1) * 2, // 更小
            data: data.map((d: any) => [d.recency, d.frequency, d.monetary, d.cluster]),
            encode: { tooltip: [0, 1, 2, 3] },
            itemStyle: {
                color: (params: any) => clusterColors[params.value[3] % clusterColors.length],
                opacity: 0.4 // 更透明
            }
        }]
    }
})
</script>