<template>
  <div class="config-page" v-loading="loading">
    <!-- 页面标题 -->
    <div class="page-header">
      <h2>系统配置管理</h2>
      <el-space>
        <el-button @click="loadConfig" :loading="loading" type="primary">
          <el-icon><Refresh /></el-icon>
          刷新配置
        </el-button>
        <el-button @click="saveConfig" :loading="saving" type="success">
          <el-icon><Check /></el-icon>
          保存配置
        </el-button>
        <el-button @click="resetConfig" type="warning">
          <el-icon><RefreshLeft /></el-icon>
          恢复默认
        </el-button>
      </el-space>
    </div>

    <!-- 配置选项卡 -->
    <el-tabs v-model="activeTab" type="border-card">
      <!-- 1. 积分获取配置 -->
      <el-tab-pane label="积分获取" name="points">
        <el-form :model="config.trading" label-width="180px" class="config-form">
          <h3 class="section-title">
            <el-icon><Trophy /></el-icon>
            积分目标
          </h3>
          <el-form-item label="每日目标积分">
            <el-input-number
              v-model="config.trading.target_points_per_day"
              :min="1"
              :max="100"
              :precision="0"
            />
            <span class="help-text">系统会根据此目标自动调整交易策略</span>
          </el-form-item>

          <el-form-item label="每日最大交易次数">
            <el-input-number
              v-model="config.trading.max_trade_count"
              :min="10"
              :max="200"
              :precision="0"
            />
            <span class="help-text">防止过度交易，保护账户</span>
          </el-form-item>

          <el-divider />

          <h3 class="section-title">
            <el-icon><Money /></el-icon>
            订单参数
          </h3>

          <el-form-item label="最小订单价值">
            <el-input-number
              v-model="config.trading.min_order_value"
              :min="1"
              :max="1000"
              :precision="2"
            />
            <span class="unit">USDT</span>
          </el-form-item>

          <el-form-item label="最大订单价值">
            <el-input-number
              v-model="config.trading.max_order_value"
              :min="10"
              :max="10000"
              :precision="2"
            />
            <span class="unit">USDT</span>
          </el-form-item>

          <el-form-item label="价格偏离度">
            <el-input-number
              v-model="config.trading.price_deviation"
              :min="0.0001"
              :max="0.1"
              :precision="4"
              :step="0.0001"
            />
            <span class="help-text">允许的价格偏离范围，降低被检测风险</span>
          </el-form-item>

          <el-form-item label="检查间隔">
            <el-input-number
              v-model="config.trading.check_interval"
              :min="10"
              :max="600"
              :precision="0"
            />
            <span class="unit">秒</span>
          </el-form-item>
        </el-form>
      </el-tab-pane>

      <!-- 2. 阶梯设计器 -->
      <el-tab-pane label="阶梯配置" name="ladders">
        <div class="ladders-section">
          <LadderDesigner
            title="资金阶梯配置"
            v-model="config.ladders.balance_ladders"
            value-unit="USDT"
          />

          <el-divider />

          <LadderDesigner
            title="交易量阶梯配置"
            v-model="config.ladders.volume_ladders"
            value-unit="USDT"
          />

          <el-divider />

          <PointsCalculator
            :balance-ladders="config.ladders.balance_ladders"
            :volume-ladders="config.ladders.volume_ladders"
          />
        </div>
      </el-tab-pane>

      <!-- 3. 风控配置 -->
      <el-tab-pane label="风控管理" name="risk">
        <el-form :model="config.risk_control" label-width="180px" class="config-form">
          <h3 class="section-title">
            <el-icon><Warning /></el-icon>
            ATR波动率监控
          </h3>

          <el-form-item label="启用ATR监控">
            <el-switch v-model="config.risk_control.atr.enabled" />
          </el-form-item>

          <el-form-item label="ATR周期">
            <el-input-number
              v-model="config.risk_control.atr.period"
              :min="5"
              :max="50"
              :precision="0"
              :disabled="!config.risk_control.atr.enabled"
            />
            <span class="help-text">计算ATR的K线周期数</span>
          </el-form-item>

          <el-form-item label="ATR倍数">
            <el-input-number
              v-model="config.risk_control.atr.multiplier"
              :min="0.5"
              :max="5"
              :precision="1"
              :step="0.1"
              :disabled="!config.risk_control.atr.enabled"
            />
            <span class="help-text">止损距离 = ATR × 倍数</span>
          </el-form-item>

          <el-form-item label="检查间隔">
            <el-input-number
              v-model="config.risk_control.atr.interval"
              :min="60"
              :max="3600"
              :precision="0"
              :disabled="!config.risk_control.atr.enabled"
            />
            <span class="unit">秒</span>
          </el-form-item>

          <el-divider />

          <h3 class="section-title">
            <el-icon><Coin /></el-icon>
            持仓限制
          </h3>

          <el-form-item label="最大总持仓价值">
            <el-input-number
              v-model="config.risk_control.position.max_total_value"
              :min="100"
              :max="100000"
              :precision="0"
            />
            <span class="unit">USDT</span>
          </el-form-item>

          <el-form-item label="单币种最大持仓">
            <el-input-number
              v-model="config.risk_control.position.max_single_value"
              :min="10"
              :max="10000"
              :precision="0"
            />
            <span class="unit">USDT</span>
          </el-form-item>

          <el-divider />

          <h3 class="section-title">
            <el-icon><DataLine /></el-icon>
            每日限额
          </h3>

          <el-form-item label="每日最大亏损">
            <el-input-number
              v-model="config.risk_control.daily_limits.max_loss"
              :min="10"
              :max="10000"
              :precision="0"
            />
            <span class="unit">USDT</span>
          </el-form-item>

          <el-form-item label="每日最大交��额">
            <el-input-number
              v-model="config.risk_control.daily_limits.max_volume"
              :min="100"
              :max="100000"
              :precision="0"
            />
            <span class="unit">USDT</span>
          </el-form-item>
        </el-form>
      </el-tab-pane>

      <!-- 4. 行为模拟 -->
      <el-tab-pane label="行为模拟" name="behavior">
        <el-form :model="config.behavior" label-width="180px" class="config-form">
          <h3 class="section-title">
            <el-icon><Timer /></el-icon>
            随机延迟
          </h3>

          <el-form-item label="启用随机延迟">
            <el-switch v-model="config.behavior.random_delay.enabled" />
            <span class="help-text">模拟人类操作的自然延迟</span>
          </el-form-item>

          <el-form-item label="最小延迟">
            <el-input-number
              v-model="config.behavior.random_delay.min"
              :min="0.5"
              :max="10"
              :precision="1"
              :step="0.5"
              :disabled="!config.behavior.random_delay.enabled"
            />
            <span class="unit">秒</span>
          </el-form-item>

          <el-form-item label="最大延迟">
            <el-input-number
              v-model="config.behavior.random_delay.max"
              :min="1"
              :max="30"
              :precision="1"
              :step="0.5"
              :disabled="!config.behavior.random_delay.enabled"
            />
            <span class="unit">秒</span>
          </el-form-item>

          <el-divider />

          <h3 class="section-title">
            <el-icon><Mouse /></el-icon>
            鼠标模拟
          </h3>

          <el-form-item label="启用鼠标模拟">
            <el-switch v-model="config.behavior.mouse_simulation.enabled" />
            <span class="help-text">模拟人类的鼠标移动轨迹</span>
          </el-form-item>

          <el-form-item label="鼠标速度">
            <el-radio-group
              v-model="config.behavior.mouse_simulation.speed"
              :disabled="!config.behavior.mouse_simulation.enabled"
            >
              <el-radio label="slow">慢速</el-radio>
              <el-radio label="medium">中速</el-radio>
              <el-radio label="fast">快速</el-radio>
            </el-radio-group>
          </el-form-item>

          <el-divider />

          <h3 class="section-title">
            <el-icon><View /></el-icon>
            页面滚动
          </h3>

          <el-form-item label="启用页面滚动">
            <el-switch v-model="config.behavior.page_scroll.enabled" />
          </el-form-item>

          <el-form-item label="滚动概率">
            <el-slider
              v-model="scrollProbability"
              :min="0"
              :max="100"
              :step="5"
              show-stops
              :marks="{ 0: '0%', 50: '50%', 100: '100%' }"
              :disabled="!config.behavior.page_scroll.enabled"
            />
          </el-form-item>
        </el-form>
      </el-tab-pane>

      <!-- 5. 通知配置 -->
      <el-tab-pane label="通知设置" name="notifications">
        <el-form :model="config.notifications" label-width="180px" class="config-form">
          <h3 class="section-title">
            <el-icon><ChatDotRound /></el-icon>
            Discord 通知
          </h3>

          <el-form-item label="启用Discord">
            <el-switch v-model="config.notifications.discord.enabled" />
          </el-form-item>

          <el-form-item label="Webhook URL">
            <el-input
              v-model="config.notifications.discord.webhook"
              placeholder="https://discord.com/api/webhooks/..."
              :disabled="!config.notifications.discord.enabled"
            />
          </el-form-item>

          <el-divider />

          <h3 class="section-title">
            <el-icon><ChatLineRound /></el-icon>
            Telegram 通知
          </h3>

          <el-form-item label="启用Telegram">
            <el-switch v-model="config.notifications.telegram.enabled" />
          </el-form-item>

          <el-form-item label="Bot Token">
            <el-input
              v-model="config.notifications.telegram.bot_token"
              placeholder="123456:ABC-DEF..."
              :disabled="!config.notifications.telegram.enabled"
            />
          </el-form-item>

          <el-form-item label="Chat ID">
            <el-input
              v-model="config.notifications.telegram.chat_id"
              placeholder="-1001234567890"
              :disabled="!config.notifications.telegram.enabled"
            />
          </el-form-item>

          <el-divider />

          <h3 class="section-title">
            <el-icon><Message /></el-icon>
            Email 通知
          </h3>

          <el-form-item label="启用Email">
            <el-switch v-model="config.notifications.email.enabled" />
          </el-form-item>

          <el-form-item label="SMTP服务器">
            <el-input
              v-model="config.notifications.email.smtp_server"
              placeholder="smtp.gmail.com"
              :disabled="!config.notifications.email.enabled"
            />
          </el-form-item>

          <el-form-item label="SMTP端口">
            <el-input-number
              v-model="config.notifications.email.smtp_port"
              :min="1"
              :max="65535"
              :precision="0"
              :disabled="!config.notifications.email.enabled"
            />
          </el-form-item>

          <el-form-item label="发件邮箱">
            <el-input
              v-model="config.notifications.email.from_addr"
              placeholder="your@email.com"
              :disabled="!config.notifications.email.enabled"
            />
          </el-form-item>

          <el-form-item label="收件邮箱">
            <el-input
              v-model="config.notifications.email.to_addr"
              placeholder="notify@email.com"
              :disabled="!config.notifications.email.enabled"
            />
          </el-form-item>
        </el-form>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import {
  Refresh,
  Check,
  RefreshLeft,
  Trophy,
  Money,
  Warning,
  Coin,
  DataLine,
  Timer,
  Mouse,
  View,
  ChatDotRound,
  ChatLineRound,
  Message
} from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import LadderDesigner from '@/components/LadderDesigner.vue'
import PointsCalculator from '@/components/PointsCalculator.vue'
import type { Ladder } from '@/components/LadderDesigner.vue'
import api from '@/api'

// 当前选项卡
const activeTab = ref('points')

// 加载状态
const loading = ref(false)
const saving = ref(false)

// 配置数据
const config = reactive({
  trading: {
    target_points_per_day: 5,
    max_trade_count: 50,
    min_order_value: 10,
    max_order_value: 100,
    price_deviation: 0.001,
    check_interval: 60
  },
  ladders: {
    balance_ladders: [] as Ladder[],
    volume_ladders: [] as Ladder[]
  },
  risk_control: {
    atr: {
      enabled: true,
      period: 14,
      multiplier: 1.5,
      interval: 300
    },
    position: {
      max_total_value: 500,
      max_single_value: 100
    },
    daily_limits: {
      max_loss: 50,
      max_volume: 5000
    }
  },
  behavior: {
    random_delay: {
      enabled: true,
      min: 1,
      max: 5
    },
    mouse_simulation: {
      enabled: true,
      speed: 'medium' as 'slow' | 'medium' | 'fast'
    },
    page_scroll: {
      enabled: true,
      probability: 0.3
    }
  },
  notifications: {
    discord: {
      enabled: false,
      webhook: ''
    },
    telegram: {
      enabled: false,
      bot_token: '',
      chat_id: ''
    },
    email: {
      enabled: false,
      smtp_server: '',
      smtp_port: 587,
      from_addr: '',
      to_addr: ''
    }
  }
})

// 滚动概率（百分比表示，方便用户理解）
const scrollProbability = computed({
  get: () => config.behavior.page_scroll.probability * 100,
  set: (val: number) => {
    config.behavior.page_scroll.probability = val / 100
  }
})

// 加载配置
const loadConfig = async () => {
  loading.value = true
  try {
    const response = await api.get('/api/config')

    if (response.data.code === 200) {
      const data = response.data.data

      // 更新交易配置
      if (data.trading) {
        Object.assign(config.trading, data.trading)
      }

      // 更新阶梯配置
      if (data.ladders) {
        config.ladders.balance_ladders = data.ladders.balance_ladders || []
        config.ladders.volume_ladders = data.ladders.volume_ladders || []
      }

      // 更新风控配置
      if (data.risk_control) {
        Object.assign(config.risk_control, data.risk_control)
      }

      // 更新行为模拟配置
      if (data.behavior) {
        Object.assign(config.behavior, data.behavior)
      }

      // 更新通知配置
      if (data.notifications) {
        Object.assign(config.notifications, data.notifications)
      }

      ElMessage.success('配置加载成功')
    }
  } catch (error) {
    console.error('加载配置失败:', error)
    ElMessage.error('配置加载失败')
  } finally {
    loading.value = false
  }
}

// 保存配置
const saveConfig = async () => {
  saving.value = true
  try {
    const response = await api.put('/api/config', {
      config: {
        trading: config.trading,
        ladders: config.ladders,
        risk_control: config.risk_control,
        behavior: config.behavior,
        notifications: config.notifications
      }
    })

    if (response.data.code === 200) {
      ElMessage.success('配置保存成功')
    }
  } catch (error: any) {
    console.error('保存配置失败:', error)
    ElMessage.error(error.response?.data?.detail || '配置保存失败')
  } finally {
    saving.value = false
  }
}

// 重置配置
const resetConfig = async () => {
  try {
    await ElMessageBox.confirm('确定要恢复默认配置吗？当前的修改将会丢失。', '确认重置', {
      type: 'warning',
      confirmButtonText: '确定',
      cancelButtonText: '取消'
    })

    await loadConfig()
    ElMessage.success('已恢复默认配置')
  } catch (error) {
    // 用户取消
  }
}

// 初始加载
onMounted(() => {
  loadConfig()
})
</script>

<style scoped lang="scss">
.config-page {
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

  .config-form {
    max-width: 800px;
    padding: 20px;

    .section-title {
      display: flex;
      align-items: center;
      gap: 8px;
      margin: 20px 0 15px;
      font-size: 16px;
      color: #303133;

      &:first-child {
        margin-top: 0;
      }
    }

    .unit,
    .help-text {
      margin-left: 10px;
      font-size: 13px;
      color: #909399;
    }
  }

  .ladders-section {
    padding: 20px;

    > div {
      margin-bottom: 30px;

      &:last-child {
        margin-bottom: 0;
      }
    }
  }

  :deep(.el-tabs__content) {
    overflow: visible;
  }

  :deep(.el-form-item__content) {
    display: flex;
    align-items: center;
  }
}
</style>
