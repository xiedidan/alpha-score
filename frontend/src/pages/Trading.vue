<template>
  <div class="trading-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <h2>交易监控</h2>
      <el-space>
        <el-tag :type="wsConnected ? 'success' : 'danger'" size="large">
          <el-icon><Connection /></el-icon>
          {{ wsConnected ? 'WebSocket 已连接' : 'WebSocket 断开' }}
        </el-tag>
        <el-button
          @click="toggleConnection"
          :type="wsConnected ? 'danger' : 'success'"
          size="default"
        >
          {{ wsConnected ? '断开连接' : '连接' }}
        </el-button>
        <el-button @click="refreshData" :loading="loading" type="primary" size="default">
          <el-icon><Refresh /></el-icon>
          刷新数据
        </el-button>
      </el-space>
    </div>

    <!-- 第一行: K线图 + 盘口深度 -->
    <el-row :gutter="20" class="chart-row">
      <el-col :xs="24" :sm="24" :md="16" :lg="16">
        <KLineChart :data="klineData" :trade-markers="tradeMarkers" :loading="loading" />
      </el-col>
      <el-col :xs="24" :sm="24" :md="8" :lg="8">
        <DepthChart :orderbook="orderbookData" :loading="loading" />
      </el-col>
    </el-row>

    <!-- 第二行: 技术指标卡片 -->
    <el-row :gutter="20" class="indicators-row">
      <el-col :xs="24" :sm="12" :md="6" :lg="6">
        <el-card shadow="hover" class="indicator-card">
          <div class="indicator-content">
            <div class="indicator-label">当前价格</div>
            <div class="indicator-value price">{{ currentPrice.toFixed(4) }} USDT</div>
            <div
              class="indicator-change"
              :class="priceChange >= 0 ? 'positive' : 'negative'"
            >
              {{ priceChange >= 0 ? '+' : '' }}{{ priceChange.toFixed(2) }}%
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6" :lg="6">
        <el-card shadow="hover" class="indicator-card">
          <div class="indicator-content">
            <div class="indicator-label">24H成交量</div>
            <div class="indicator-value">{{ volume24h.toFixed(2) }}</div>
            <div class="indicator-unit">USDT</div>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6" :lg="6">
        <el-card shadow="hover" class="indicator-card">
          <div class="indicator-content">
            <div class="indicator-label">ATR (波动率)</div>
            <div class="indicator-value">{{ atr.toFixed(6) }}</div>
            <div class="indicator-unit">USDT</div>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6" :lg="6">
        <el-card shadow="hover" class="indicator-card">
          <div class="indicator-content">
            <div class="indicator-label">今日交易次数</div>
            <div class="indicator-value">{{ todayTradesCount }}</div>
            <div class="indicator-unit">笔</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 第三行: 交易列表 -->
    <div class="table-row">
      <TradeTable :trades="tradeRecords" :loading="loading" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { Connection, Refresh } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import TradeTable from '@/components/TradeTable.vue'
import KLineChart from '@/components/KLineChart.vue'
import DepthChart from '@/components/DepthChart.vue'
import { useTradingWebSocket } from '@/composables/useTradingWebSocket'
import type { TradeRecord } from '@/components/TradeTable.vue'
import type { KLineData, TradeMarker } from '@/components/KLineChart.vue'
import type { OrderbookData } from '@/components/DepthChart.vue'

// WebSocket连接
const {
  isConnected: wsConnected,
  latestPrice,
  latestOrderbook,
  latestTrade,
  connect,
  disconnect
} = useTradingWebSocket()

// 数据状态
const loading = ref(false)
const klineData = ref<KLineData[]>([])
const orderbookData = ref<OrderbookData>({
  bids: [],
  asks: []
})
const tradeRecords = ref<TradeRecord[]>([])
const tradeMarkers = ref<TradeMarker[]>([])

// 技术指标
const currentPrice = ref(0)
const priceChange = ref(0)
const volume24h = ref(0)
const atr = ref(0)

// 今日交易次数
const todayTradesCount = computed(() => {
  const today = new Date().toDateString()
  return tradeRecords.value.filter(
    (trade) => new Date(trade.timestamp).toDateString() === today
  ).length
})

// 切换WebSocket连接
const toggleConnection = () => {
  if (wsConnected.value) {
    disconnect()
    ElMessage.warning('WebSocket连接已断开')
  } else {
    connect()
    ElMessage.success('WebSocket连接已建立')
  }
}

// 刷新数据
const refreshData = async () => {
  loading.value = true
  try {
    await loadMockData()
    ElMessage.success('数据已刷新')
  } catch (error) {
    ElMessage.error('数据刷新失败')
    console.error('刷新数据失败:', error)
  } finally {
    loading.value = false
  }
}

// 加载模拟数据（实际使用时替换为API调用）
const loadMockData = async () => {
  // 模拟延迟
  await new Promise((resolve) => setTimeout(resolve, 500))

  // 生成K线数据
  const now = Date.now()
  const basePrice = 43250
  klineData.value = Array.from({ length: 100 }, (_, i) => {
    const timestamp = new Date(now - (99 - i) * 60000).toISOString()
    const random = () => (Math.random() - 0.5) * 100
    const open = basePrice + random()
    const close = open + random()
    const high = Math.max(open, close) + Math.abs(random()) / 2
    const low = Math.min(open, close) - Math.abs(random()) / 2
    const volume = Math.random() * 1000 + 500

    return { timestamp, open, close, low, high, volume }
  })

  // 生成盘口数据
  const midPrice = basePrice
  orderbookData.value = {
    bids: Array.from({ length: 20 }, (_, i) => ({
      price: midPrice - (i + 1) * 5,
      quantity: Math.random() * 10 + 1
    })),
    asks: Array.from({ length: 20 }, (_, i) => ({
      price: midPrice + (i + 1) * 5,
      quantity: Math.random() * 10 + 1
    }))
  }

  // 生成交易记录
  tradeRecords.value = Array.from({ length: 100 }, (_, i) => ({
    id: `trade-${i}`,
    timestamp: new Date(now - (99 - i) * 300000).toISOString(),
    side: Math.random() > 0.5 ? 'buy' : 'sell',
    symbol: 'BTC/USDT',
    price: basePrice + (Math.random() - 0.5) * 200,
    quantity: Math.random() * 0.1 + 0.01,
    cost: 0,
    points: Math.floor(Math.random() * 10) + 1,
    status: Math.random() > 0.1 ? 'success' : Math.random() > 0.5 ? 'pending' : 'failed',
    note: Math.random() > 0.7 ? '自动交易' : undefined
  }))

  // 计算成交额
  tradeRecords.value.forEach((trade) => {
    trade.cost = trade.price * trade.quantity
  })

  // 生成交易标记（最近10笔成功的交易）
  tradeMarkers.value = tradeRecords.value
    .filter((t) => t.status === 'success')
    .slice(-10)
    .map((t) => ({
      timestamp: t.timestamp,
      price: t.price,
      type: t.side,
      note: `${t.side === 'buy' ? '买入' : '卖出'} ${t.quantity.toFixed(4)}`
    }))

  // 更新技术指标
  currentPrice.value = klineData.value[klineData.value.length - 1]?.close || 0
  const firstPrice = klineData.value[0]?.open || currentPrice.value
  priceChange.value = ((currentPrice.value - firstPrice) / firstPrice) * 100
  volume24h.value = tradeRecords.value.reduce((sum, t) => sum + t.cost, 0)

  // 计算ATR (简化版本)
  const trueRanges = klineData.value.slice(-14).map((k) => k.high - k.low)
  atr.value = trueRanges.reduce((sum, tr) => sum + tr, 0) / trueRanges.length
}

// WebSocket数据更新处理
const handleWebSocketUpdates = () => {
  // 监听价格更新
  if (latestPrice.value) {
    currentPrice.value = latestPrice.value.price
    priceChange.value = latestPrice.value.change_24h
  }

  // 监听盘口更新
  if (latestOrderbook.value) {
    orderbookData.value = {
      bids: latestOrderbook.value.bids.map(([price, quantity]) => ({ price, quantity })),
      asks: latestOrderbook.value.asks.map(([price, quantity]) => ({ price, quantity }))
    }
  }

  // 监听交易执行
  if (latestTrade.value) {
    const newTrade: TradeRecord = {
      id: `trade-${Date.now()}`,
      timestamp: new Date().toISOString(),
      side: latestTrade.value.side,
      symbol: 'BTC/USDT',
      price: latestTrade.value.price,
      quantity: latestTrade.value.quantity,
      cost: latestTrade.value.cost,
      points: Math.floor(Math.random() * 10) + 1,
      status: 'success',
      note: '实时交易'
    }

    // 添加到列表顶部
    tradeRecords.value.unshift(newTrade)
    // 保持最多100条记录
    if (tradeRecords.value.length > 100) {
      tradeRecords.value.pop()
    }

    // 添加交易标记
    tradeMarkers.value.push({
      timestamp: newTrade.timestamp,
      price: newTrade.price,
      type: newTrade.side
    })

    ElMessage.success(`${newTrade.side === 'buy' ? '买入' : '卖出'}交易执行成功`)
  }
}

// 生命周期
onMounted(async () => {
  // 连接WebSocket
  connect()

  // 加载初始数据
  await refreshData()

  // 设置WebSocket数据更新监听
  setInterval(handleWebSocketUpdates, 1000)
})

onUnmounted(() => {
  disconnect()
})
</script>

<style scoped lang="scss">
.trading-page {
  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    padding-bottom: 15px;
    border-bottom: 2px solid #ebeef5;

    h2 {
      margin: 0;
      font-size: 24px;
      font-weight: bold;
      color: #303133;
    }
  }

  .chart-row {
    margin-bottom: 20px;
  }

  .indicators-row {
    margin-bottom: 20px;

    .indicator-card {
      height: 100%;

      .indicator-content {
        text-align: center;
        padding: 10px 0;

        .indicator-label {
          font-size: 14px;
          color: #909399;
          margin-bottom: 10px;
        }

        .indicator-value {
          font-size: 28px;
          font-weight: bold;
          color: #303133;
          margin-bottom: 5px;

          &.price {
            color: #409eff;
          }
        }

        .indicator-change {
          font-size: 14px;
          font-weight: 600;

          &.positive {
            color: #67c23a;
          }

          &.negative {
            color: #f56c6c;
          }
        }

        .indicator-unit {
          font-size: 12px;
          color: #c0c4cc;
        }
      }
    }
  }

  .table-row {
    margin-top: 20px;
  }
}
</style>
