<template>
    <EchartBase :option="option" height="400px" />
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import EchartBase from '../components/EchartBase.vue'

const option = ref({})

onMounted(async () => {
    const res = await fetch('/category_cooccurrence.json')
    const data = await res.json()
    // 获取所有品类
    const cats = Array.from(new Set(data.flatMap((d: any) => [d.cat1, d.cat2])))
    // 构建热力图数据
    const matrix = cats.map((c1, i) =>
        cats.map((c2, j) => {
            const found = data.find((d: any) => d.cat1 === c1 && d.cat2 === c2)
            return found ? found.count : 0
        })
    )
    option.value = {
        title: { text: '品类关联热力图', left: 'center' },
        tooltip: { position: 'top' },
        xAxis: { type: 'category', data: cats },
        yAxis: { type: 'category', data: cats },
        visualMap: { min: 0, max: Math.max(...matrix.flat()), calculable: true, orient: 'vertical', right: 0, top: 'center' },
        series: [{
            name: '共现次数',
            type: 'heatmap',
            data: matrix.flatMap((row, i) => row.map((v, j) => [i, j, v])),
            label: { show: false }
        }]
    }
})
</script>