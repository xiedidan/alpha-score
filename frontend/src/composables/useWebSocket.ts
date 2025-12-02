/**
 * WebSocket客户端 Composable
 * 用于与后端WebSocket服务通信
 */
import { ref, onUnmounted } from 'vue'
import { logger } from '@/utils/logger'

export interface WebSocketMessage {
  type: string
  data: any
  timestamp: string
}

export interface WebSocketOptions {
  onMessage?: (message: WebSocketMessage) => void
  onConnected?: () => void
  onDisconnected?: () => void
  onError?: (error: Event) => void
  autoReconnect?: boolean
  reconnectInterval?: number
}

export function useWebSocket(url: string, options: WebSocketOptions = {}) {
  const {
    onMessage,
    onConnected,
    onDisconnected,
    onError,
    autoReconnect = true,
    reconnectInterval = 3000
  } = options

  const ws = ref<WebSocket | null>(null)
  const isConnected = ref(false)
  const reconnectTimer = ref<number | null>(null)

  /**
   * 连接WebSocket
   */
  const connect = () => {
    if (ws.value) {
      logger.warn('WebSocket已连接，跳过重复连接')
      return
    }

    try {
      ws.value = new WebSocket(url)

      ws.value.onopen = () => {
        logger.info('WebSocket连接成功')
        isConnected.value = true
        onConnected?.()

        // 清除重连定时器
        if (reconnectTimer.value) {
          clearTimeout(reconnectTimer.value)
          reconnectTimer.value = null
        }
      }

      ws.value.onmessage = (event) => {
        try {
          const message: WebSocketMessage = JSON.parse(event.data)
          logger.debug('收到WebSocket消息:', message.type)

          // 处理心跳
          if (message.type === 'ping') {
            ws.value?.send('pong')
            logger.debug('发送pong响应')
            return
          }

          // 触发消息回调
          onMessage?.(message)
        } catch (error) {
          logger.error('解析WebSocket消息失败:', error)
        }
      }

      ws.value.onerror = (event) => {
        logger.error('WebSocket错误:', event)
        onError?.(event)
      }

      ws.value.onclose = () => {
        logger.info('WebSocket连接关闭')
        isConnected.value = false
        ws.value = null
        onDisconnected?.()

        // 自动重连
        if (autoReconnect && !reconnectTimer.value) {
          reconnectTimer.value = window.setTimeout(() => {
            logger.info('尝试重新连接WebSocket...')
            reconnectTimer.value = null
            connect()
          }, reconnectInterval)
        }
      }
    } catch (error) {
      logger.error('WebSocket连接失败:', error)
      onError?.(error as Event)
    }
  }

  /**
   * 断开WebSocket连接
   */
  const disconnect = () => {
    if (reconnectTimer.value) {
      clearTimeout(reconnectTimer.value)
      reconnectTimer.value = null
    }

    if (ws.value) {
      ws.value.close()
      ws.value = null
      isConnected.value = false
      logger.info('WebSocket主动断开')
    }
  }

  /**
   * 发送消息
   */
  const send = (data: string | object) => {
    if (!ws.value || !isConnected.value) {
      logger.error('WebSocket未连接，无法发送消息')
      return false
    }

    try {
      const message = typeof data === 'string' ? data : JSON.stringify(data)
      ws.value.send(message)
      return true
    } catch (error) {
      logger.error('发送WebSocket消息失败:', error)
      return false
    }
  }

  // 组件卸载时自动断开
  onUnmounted(() => {
    disconnect()
  })

  return {
    isConnected,
    connect,
    disconnect,
    send
  }
}
