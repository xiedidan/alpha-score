<template>
  <div class="kline-chart">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <el-icon><TrendCharts /></el-icon>
          <span>K线图表</span>
        </div>
      </template>

      <div class="chart-container">
        <v-chart
          ref="chartRef"
          :option="chartOption"
          :loading="loading"
          autoresize
          :style="{ height: '500px' }"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { CandlestickChart, LineChart, ScatterChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  DataZoomComponent,
  MarkPointComponent
} from 'echarts/components'
import VChart from 'vue-echarts'
import { TrendCharts } from '@element-plus/icons-vue'

use([
  CanvasRenderer,
  CandlestickChart,
  LineChart,
  ScatterChart,
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  DataZoomComponent,
  MarkPointComponent
])

// K线数据类型
export interface KLineData {
  timestamp: string
  open: number
  close: number
  low: number
  high: number
  volume: number
}

// 交易标记类型
export interface TradeMarker {
  timestamp: string
  price: number
  type: 'buy' | 'sell'
  note?: string
}

// Props
const props = defineProps<{
  data: KLineData[]
  tradeMarkers?: TradeMarker[]
  loading?: boolean
}>()

const chartRef = ref<InstanceType<typeof VChart>>()

// 处理K线数据
const processedData = computed(() => {
  const times: string[] = []
  const values: [number, number, number, number][] = []
  const volumes: number[] = []

  props.data.forEach((item) => {
    times.push(
      new Date(item.timestamp).toLocaleString('zh-CN', {
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    )
    values.push([item.open, item.close, item.low, item.high])
    volumes.push(item.volume)
  })

  return { times, values, volumes }
})

// 处理交易标记
const buyMarkers = computed(() => {
  if (!props.tradeMarkers) return []
  return props.tradeMarkers
    .filter((m) => m.type === 'buy')
    .map((m) => ({
      name: '买入',
      coord: [
        new Date(m.timestamp).toLocaleString('zh-CN', {
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit'
        }),
        m.price
      ],
      value: m.price.toFixed(4),
      itemStyle: { color: '#67c23a' }
    }))
})

const sellMarkers = computed(() => {
  if (!props.tradeMarkers) return []
  return props.tradeMarkers
    .filter((m) => m.type === 'sell')
    .map((m) => ({
      name: '卖出',
      coord: [
        new Date(m.timestamp).toLocaleString('zh-CN', {
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit'
        }),
        m.price
      ],
      value: m.price.toFixed(4),
      itemStyle: { color: '#f56c6c' }
    }))
})

// 图表配置
const chartOption = computed(() => ({
  animation: true,
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'cross'
    },
    formatter: (params: any) => {
      const data = params[0]
      if (!data) return ''

      const klineData = data.data
      const volumeData = params[1]?.data

      return `
        <div style="padding: 5px;">
          <div style="font-weight: bold; margin-bottom: 5px;">${data.axisValue}</div>
          <div style="display: flex; justify-content: space-between; gap: 20px;">
            <div>
              <div>开盘: <span style="color: ${klineData[0] > klineData[1] ? '#f56c6c' : '#67c23a'}">${klineData[0]?.toFixed(4)}</span></div>
              <div>收盘: <span style="color: ${klineData[0] > klineData[1] ? '#f56c6c' : '#67c23a'}">${klineData[1]?.toFixed(4)}</span></div>
              <div>最低: ${klineData[2]?.toFixed(4)}</div>
              <div>最高: ${klineData[3]?.toFixed(4)}</div>
            </div>
            ${volumeData ? `<div>成交量: ${volumeData.toFixed(2)}</div>` : ''}
          </div>
        </div>
      `
    }
  },
  grid: [
    {
      left: '5%',
      right: '5%',
      top: '8%',
      height: '60%'
    },
    {
      left: '5%',
      right: '5%',
      top: '75%',
      height: '15%'
    }
  ],
  xAxis: [
    {
      type: 'category',
      data: processedData.value.times,
      scale: true,
      boundaryGap: true,
      axisLine: { onZero: false },
      splitLine: { show: false },
      min: 'dataMin',
      max: 'dataMax'
    },
    {
      type: 'category',
      gridIndex: 1,
      data: processedData.value.times,
      scale: true,
      boundaryGap: true,
      axisLine: { onZero: false },
      splitLine: { show: false },
      min: 'dataMin',
      max: 'dataMax',
      axisLabel: { show: false }
    }
  ],
  yAxis: [
    {
      scale: true,
      splitArea: {
        show: true
      },
      axisLabel: {
        formatter: (value: number) => value.toFixed(4)
      }
    },
    {
      scale: true,
      gridIndex: 1,
      splitNumber: 2,
      axisLabel: { show: false },
      axisLine: { show: false },
      axisTick: { show: false },
      splitLine: { show: false }
    }
  ],
  dataZoom: [
    {
      type: 'inside',
      xAxisIndex: [0, 1],
      start: 0,
      end: 100
    },
    {
      show: true,
      xAxisIndex: [0, 1],
      type: 'slider',
      top: '92%',
      start: 0,
      end: 100
    }
  ],
  series: [
    {
      name: 'K线',
      type: 'candlestick',
      data: processedData.value.values,
      itemStyle: {
        color: '#ef5350',
        color0: '#26a69a',
        borderColor: '#ef5350',
        borderColor0: '#26a69a'
      },
      markPoint: {
        symbol: 'pin',
        symbolSize: 50,
        data: [...buyMarkers.value, ...sellMarkers.value],
        label: {
          formatter: (param: any) => {
            return param.value
          }
        }
      }
    },
    {
      name: '成交量',
      type: 'bar',
      xAxisIndex: 1,
      yAxisIndex: 1,
      data: processedData.value.volumes,
      itemStyle: {
        color: (params: any) => {
          const colorList = ['#ef5350', '#26a69a']
          const idx = processedData.value.values[params.dataIndex]
          return idx && idx[0] > idx[1] ? colorList[0] : colorList[1]
        }
      }
    }
  ]
}))

// 监听数据变化，更新图表
watch(
  () => props.data,
  () => {
    if (chartRef.value) {
      chartRef.value.setOption(chartOption.value)
    }
  },
  { deep: true }
)
</script>

<style scoped lang="scss">
.kline-chart {
  .card-header {
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: bold;
  }

  .chart-container {
    width: 100%;
  }
}
</style>
