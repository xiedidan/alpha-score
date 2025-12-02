<template>
  <div class="depth-chart">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <el-icon><DataAnalysis /></el-icon>
          <span>盘口深度</span>
        </div>
      </template>

      <div class="chart-container">
        <v-chart
          ref="chartRef"
          :option="chartOption"
          :loading="loading"
          autoresize
          :style="{ height: '400px' }"
        />
      </div>

      <!-- 实时数据展示 -->
      <div class="depth-stats">
        <el-row :gutter="20">
          <el-col :span="12">
            <div class="stat-item buy">
              <span class="label">买盘总量</span>
              <span class="value">{{ totalBuyVolume.toFixed(2) }}</span>
            </div>
          </el-col>
          <el-col :span="12">
            <div class="stat-item sell">
              <span class="label">卖盘总量</span>
              <span class="value">{{ totalSellVolume.toFixed(2) }}</span>
            </div>
          </el-col>
        </el-row>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent
} from 'echarts/components'
import VChart from 'vue-echarts'
import { DataAnalysis } from '@element-plus/icons-vue'

use([
  CanvasRenderer,
  LineChart,
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent
])

// 盘口数据类型
export interface OrderbookLevel {
  price: number
  quantity: number
}

export interface OrderbookData {
  bids: OrderbookLevel[] // 买盘 [[price, quantity], ...]
  asks: OrderbookLevel[] // 卖盘 [[price, quantity], ...]
}

// Props
const props = defineProps<{
  orderbook: OrderbookData
  loading?: boolean
}>()

const chartRef = ref<InstanceType<typeof VChart>>()

// 计算累计深度
const processedBids = computed(() => {
  let cumulative = 0
  return props.orderbook.bids
    .slice()
    .reverse() // 从低价到高价
    .map((level) => {
      cumulative += level.quantity
      return {
        price: level.price,
        quantity: cumulative
      }
    })
    .reverse() // 恢复从高价到低价顺序
})

const processedAsks = computed(() => {
  let cumulative = 0
  return props.orderbook.asks.map((level) => {
    cumulative += level.quantity
    return {
      price: level.price,
      quantity: cumulative
    }
  })
})

// 统计数据
const totalBuyVolume = computed(() => {
  return props.orderbook.bids.reduce((sum, level) => sum + level.quantity, 0)
})

const totalSellVolume = computed(() => {
  return props.orderbook.asks.reduce((sum, level) => sum + level.quantity, 0)
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
      if (!params || params.length === 0) return ''

      return params
        .map((param: any) => {
          const type = param.seriesName === '买盘' ? '买盘' : '卖盘'
          const color = param.color
          return `
          <div style="margin: 5px 0;">
            <span style="display:inline-block;width:10px;height:10px;border-radius:50%;background-color:${color};margin-right:5px;"></span>
            <strong>${type}</strong>
            <div style="margin-left: 15px;">
              价格: <span style="color: ${color}">${param.data[0]?.toFixed(4)}</span><br/>
              累计量: ${param.data[1]?.toFixed(2)}
            </div>
          </div>
        `
        })
        .join('')
    }
  },
  legend: {
    data: ['买盘', '卖盘'],
    top: '2%'
  },
  grid: {
    left: '5%',
    right: '5%',
    bottom: '10%',
    top: '15%',
    containLabel: true
  },
  xAxis: {
    type: 'value',
    name: '价格 (USDT)',
    nameLocation: 'middle',
    nameGap: 30,
    axisLabel: {
      formatter: (value: number) => value.toFixed(4)
    },
    splitLine: {
      show: true,
      lineStyle: {
        type: 'dashed'
      }
    }
  },
  yAxis: {
    type: 'value',
    name: '累计数量',
    nameLocation: 'middle',
    nameGap: 50,
    axisLabel: {
      formatter: (value: number) => value.toFixed(2)
    },
    splitLine: {
      show: true,
      lineStyle: {
        type: 'dashed'
      }
    }
  },
  series: [
    {
      name: '买盘',
      type: 'line',
      data: processedBids.value.map((d) => [d.price, d.quantity]),
      smooth: false,
      symbol: 'none',
      lineStyle: {
        color: '#67c23a',
        width: 2
      },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0,
          y: 0,
          x2: 0,
          y2: 1,
          colorStops: [
            { offset: 0, color: 'rgba(103, 194, 58, 0.5)' },
            { offset: 1, color: 'rgba(103, 194, 58, 0.1)' }
          ]
        }
      },
      emphasis: {
        focus: 'series'
      }
    },
    {
      name: '卖盘',
      type: 'line',
      data: processedAsks.value.map((d) => [d.price, d.quantity]),
      smooth: false,
      symbol: 'none',
      lineStyle: {
        color: '#f56c6c',
        width: 2
      },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0,
          y: 0,
          x2: 0,
          y2: 1,
          colorStops: [
            { offset: 0, color: 'rgba(245, 108, 108, 0.5)' },
            { offset: 1, color: 'rgba(245, 108, 108, 0.1)' }
          ]
        }
      },
      emphasis: {
        focus: 'series'
      }
    }
  ]
}))

// 监听数据变化，更新图表
watch(
  () => props.orderbook,
  () => {
    if (chartRef.value) {
      chartRef.value.setOption(chartOption.value)
    }
  },
  { deep: true }
)
</script>

<style scoped lang="scss">
.depth-chart {
  .card-header {
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: bold;
  }

  .chart-container {
    width: 100%;
  }

  .depth-stats {
    margin-top: 20px;
    padding-top: 20px;
    border-top: 1px solid #ebeef5;

    .stat-item {
      padding: 15px;
      border-radius: 8px;
      display: flex;
      flex-direction: column;
      gap: 8px;

      &.buy {
        background: rgba(103, 194, 58, 0.1);
        border: 1px solid rgba(103, 194, 58, 0.3);

        .label {
          color: #67c23a;
        }

        .value {
          color: #67c23a;
        }
      }

      &.sell {
        background: rgba(245, 108, 108, 0.1);
        border: 1px solid rgba(245, 108, 108, 0.3);

        .label {
          color: #f56c6c;
        }

        .value {
          color: #f56c6c;
        }
      }

      .label {
        font-size: 14px;
        font-weight: 500;
      }

      .value {
        font-size: 24px;
        font-weight: bold;
      }
    }
  }
}
</style>
