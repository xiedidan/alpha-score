import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

// 交易数据接口定义
export interface PointsData {
  current: number
  target: number
  percentage: number
}

export interface TradingStats {
  volume: number
  count: number
  cost: number
}

export interface SystemStatus {
  mode: 'auto' | 'manual' | 'paused'
  uptime: number
  lastOperation: string
}

export interface FundsOverview {
  available: number
  position: number
  grid: number
}

export interface MarketData {
  bidPrice: number
  askPrice: number
  spread: number
  atr: number
}

export const useTradingStore = defineStore('trading', () => {
  // 今日积分数据
  const pointsData = ref<PointsData>({
    current: 0,
    target: 100,
    percentage: 0
  })

  // 今日交易统计
  const tradingStats = ref<TradingStats>({
    volume: 0,
    count: 0,
    cost: 0
  })

  // 系统运行状态
  const systemStatus = ref<SystemStatus>({
    mode: 'paused',
    uptime: 0,
    lastOperation: '-'
  })

  // 资金概览
  const fundsOverview = ref<FundsOverview>({
    available: 0,
    position: 0,
    grid: 0
  })

  // 盘口数据
  const marketData = ref<MarketData>({
    bidPrice: 0,
    askPrice: 0,
    spread: 0,
    atr: 0
  })

  // 加载状态
  const loading = ref<boolean>(false)

  // Computed: 总资产
  const totalAssets = computed(() => {
    return fundsOverview.value.available + fundsOverview.value.position + fundsOverview.value.grid
  })

  // Computed: 系统状态文本
  const systemStatusText = computed(() => {
    const statusMap = {
      auto: '自动运行',
      manual: '手动模式',
      paused: '已暂停'
    }
    return statusMap[systemStatus.value.mode] || '未知'
  })

  // Computed: 系统状态颜色
  const systemStatusType = computed(() => {
    const typeMap = {
      auto: 'success',
      manual: 'warning',
      paused: 'info'
    }
    return typeMap[systemStatus.value.mode] || 'info'
  })

  // 格式化运行时长
  const formatUptime = computed(() => {
    const hours = Math.floor(systemStatus.value.uptime / 3600)
    const minutes = Math.floor((systemStatus.value.uptime % 3600) / 60)
    return `${hours}h ${minutes}m`
  })

  // 更新积分数据
  function updatePointsData(data: Partial<PointsData>) {
    pointsData.value = { ...pointsData.value, ...data }
    pointsData.value.percentage = (pointsData.value.current / pointsData.value.target) * 100
  }

  // 更新交易统计
  function updateTradingStats(data: Partial<TradingStats>) {
    tradingStats.value = { ...tradingStats.value, ...data }
  }

  // 更新系统状态
  function updateSystemStatus(data: Partial<SystemStatus>) {
    systemStatus.value = { ...systemStatus.value, ...data }
  }

  // 更新资金概览
  function updateFundsOverview(data: Partial<FundsOverview>) {
    fundsOverview.value = { ...fundsOverview.value, ...data }
  }

  // 更新盘口数据
  function updateMarketData(data: Partial<MarketData>) {
    marketData.value = { ...marketData.value, ...data }
  }

  // 加载模拟数据（用于开发和测试）
  function loadMockData() {
    loading.value = true

    // 模拟API延迟
    setTimeout(() => {
      updatePointsData({
        current: 45,
        target: 100
      })

      updateTradingStats({
        volume: 15234.56,
        count: 128,
        cost: 12.34
      })

      updateSystemStatus({
        mode: 'auto',
        uptime: 7235,
        lastOperation: new Date().toLocaleString('zh-CN')
      })

      updateFundsOverview({
        available: 8543.21,
        position: 2456.78,
        grid: 1000.00
      })

      updateMarketData({
        bidPrice: 0.05234,
        askPrice: 0.05236,
        spread: 0.00002,
        atr: 0.00015
      })

      loading.value = false
    }, 500)
  }

  // 重置数据
  function reset() {
    pointsData.value = { current: 0, target: 100, percentage: 0 }
    tradingStats.value = { volume: 0, count: 0, cost: 0 }
    systemStatus.value = { mode: 'paused', uptime: 0, lastOperation: '-' }
    fundsOverview.value = { available: 0, position: 0, grid: 0 }
    marketData.value = { bidPrice: 0, askPrice: 0, spread: 0, atr: 0 }
  }

  return {
    // State
    pointsData,
    tradingStats,
    systemStatus,
    fundsOverview,
    marketData,
    loading,

    // Computed
    totalAssets,
    systemStatusText,
    systemStatusType,
    formatUptime,

    // Actions
    updatePointsData,
    updateTradingStats,
    updateSystemStatus,
    updateFundsOverview,
    updateMarketData,
    loadMockData,
    reset
  }
})
