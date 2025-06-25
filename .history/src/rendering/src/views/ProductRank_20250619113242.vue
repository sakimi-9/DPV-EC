<template>
    <EchartsBase :option="option" height="400px" />
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import EchartsBase from '../components/EchartBase.vue'

const option = ref({})

onMounted(async () => {
    // 读取订单明细和产品信息
    const [orderItemsRes, productsRes] = await Promise.all([
        fetch('/data/order_items.json'),
        fetch('/data/products.json')
    ])
    const orderItems = await orderItemsRes.json()
    const products = await productsRes.json()

    // 统计每个产品的销量
    const salesMap: Record<string, number> = {}
    orderItems.forEach((item: any) => {
        if (!item.product_id || !item.quantity) return
        salesMap[item.product_id] = (salesMap[item.product_id] || 0) + Number(item.quantity)
    })

    // 合并产品名称
    const productNameMap: Record<string, string> = {}
    products.forEach((prod: any) => {
        productNameMap[prod.product_id] = prod.name || prod.product_id
    })

    // 取销量前20的产品
    const topProducts = Object.entries(salesMap)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 20)
        .map(([pid, qty]) => ({
            name: productNameMap[pid] || pid,
            value: qty
        }))

    option.value = {
        title: { text: '产品销售排行（前20）' },
        tooltip: { trigger: 'axis' },
        xAxis: { type: 'category', data: topProducts.map(i => i.name), axisLabel: { rotate: 45 } },
        yAxis: { type: 'value' },
        series: [{ data: topProducts.map(i => i.value), type: 'bar' }]
    }
})
</script>