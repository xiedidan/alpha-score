/**
 * 交易WebSocket客户端
 * 专门用于接收实时交易数据
 */
import { ref } from 'vue'
import { useWebSocket, type WebSocketMessage } from './useWebSocket'
import { logger } from '@/utils/logger'

export interface PriceUpdate {
  symbol: string
  price: number
  change_24h: number
}

export interface OrderbookUpdate {
  bids: [number, number][]
  asks: [number, number][]
}

export interface TradeExecuted {
  side: 'buy' | 'sell'
  price: number
  quantity: number
  cost: number
}

export interface SystemStatus {
  mode: 'auto' | 'manual' | 'paused'
  points_today: number
  volume_today: number
}

export function useTradingWebSocket() {
  // WebSocket URL (根据环境自动切换)
  const wsUrl = import.meta.env.DEV
    ? 'ws://localhost:8000/ws'
    : `ws://${window.location.host}/ws`

  // 数据状态
  const latestPrice = ref<PriceUpdate | null>(null)
  const latestOrderbook = ref<OrderbookUpdate | null>(null)
  const latestTrade = ref<TradeExecuted | null>(null)
  const systemStatus = ref<SystemStatus | null>(null)

  // 消息处理
  const handleMessage = (message: WebSocketMessage) => {
    switch (message.type) {
      case 'connection_established':
        logger.info('WebSocket连接已建立:', message.data)
        break

      case 'price_update':
        latestPrice.value = message.data
        logger.debug('价格更新:', message.data)
        break

      case 'orderbook_update':
        latestOrderbook.value = message.data
        logger.debug('盘口更新')
        break

      case 'trade_executed':
        latestTrade.value = message.data
        logger.info('交易执行:', message.data)
        break

      case 'system_status':
        systemStatus.value = message.data
        logger.debug('系统状态:', message.data)
        break

      case 'echo':
        logger.debug('服务器回显:', message.data)
        break

      default:
        logger.warn('未知消息类型:', message.type)
    }
  }

  // 创建WebSocket连接
  const { isConnected, connect, disconnect, send } = useWebSocket(wsUrl, {
    onMessage: handleMessage,
    onConnected: () => {
      logger.info('交易WebSocket已连接')
    },
    onDisconnected: () => {
      logger.warn('交易WebSocket已断开')
    },
    onError: (error) => {
      logger.error('交易WebSocket错误:', error)
    },
    autoReconnect: true,
    reconnectInterval: 3000
  })

  return {
    // 连接状态
    isConnected,

    // 数据
    latestPrice,
    latestOrderbook,
    latestTrade,
    systemStatus,

    // 方法
    connect,
    disconnect,
    send
  }
}
