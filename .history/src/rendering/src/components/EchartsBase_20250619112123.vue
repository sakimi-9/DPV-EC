<template>
    <div ref="chartRef" :style="{ width: '100%', height: height }"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
    option: { type: Object, required: true },
    height: { type: String, default: '400px' }
})

const chartRef = ref<HTMLElement | null>(null)
let chartInstance: echarts.ECharts | null = null

const renderChart = () => {
    if (chartRef.value) {
        if (!chartInstance) {
            chartInstance = echarts.init(chartRef.value)
        }
        chartInstance.setOption(props.option)
    }
}

onMounted(() => {
    renderChart()
    window.addEventListener('resize', resizeChart)
})

onBeforeUnmount(() => {
    if (chartInstance) {
        chartInstance.dispose()
        chartInstance = null
    }
    window.removeEventListener('resize', resizeChart)
})

const resizeChart = () => {
    if (chartInstance) {
        chartInstance.resize()
    }
}

watch(() => props.option, renderChart, { deep: true })
</script>