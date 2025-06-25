<template>
    <EchartBase :option="option" height="400px" />
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import EchartBase from '../components/EchartBase.vue'

const option = ref({})

const clusterColors = ['#5470C6', '#91CC75', '#FAC858', '#EE6666', '#73C0DE', '#3BA272']

onMounted(async () => {
    const res = await fetch('/rfm_scatter.json')
    const data = await res.json()
    // 按聚类分组
    const clusters = Array.from(new Set(data.map((d: any) => d.cluster))) as number[]
    const series = clusters.map((c: number, idx: number) => ({
        name: `集群${c + 1}`,
        type: 'scatter',
        data: data.filter((d: any) => d.cluster === c).map((d: any) => [d.x, d.y]),
        emphasis: { focus: 'series' },
        color: clusterColors[idx % clusterColors.length]
    }))
    option.value = {
        title: { text: '用户价值分群（RFM聚类散点）', left: 'center' },
        tooltip: { trigger: 'item', formatter: (p: any) => `x: ${p.value[0].toFixed(2)}<br/>y: ${p.value[1].toFixed(2)}` },
        legend: { data: series.map(s => s.name), top: 30 },
        xAxis: {},
        yAxis: {},
        series
    }
})
</script>