<template>
    <EchartBase :option="option" height="400px" />
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import EchartBase from '../components/EchartBase.vue'

const option = ref({})

onMounted(async () => {
    // 读取订单明细和产品信息
    const [orderItemsRes, productsRes] = await Promise.all([
        fetch('/order_items.json'),
        fetch('/products.json')
    ])
    const orderItems = await orderItemsRes.json()
    const products = await productsRes.json()
    // 构建产品ID到品类的映射
    const prodCatMap: Record<string, string> = {}
    products.forEach((p: any) => { prodCatMap[p.product_id] = p.category })
    // 统计每个品类的销售额
    const catSales: Record<string, number> = {}
    orderItems.forEach((item: any) => {
        const cat = prodCatMap[item.product_id] || '未知'
        const amount = Number(item.price) * Number(item.quantity)
        catSales[cat] = (catSales[cat] || 0) + amount
    })
    const cats = Object.keys(catSales)
    option.value = {
        title: { text: '各品类销售额' },
        tooltip: { trigger: 'axis' },
        xAxis: { type: 'category', data: cats, axisLabel: { rotate: 30 } },
        yAxis: { type: 'value' },
        series: [{ data: cats.map(c => catSales[c]), type: 'bar' }]
    }
})
</script>