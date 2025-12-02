<template>
  <div class="dashboard" v-loading="tradingStore.loading">
    <!-- 顶部标题行 -->
    <div class="dashboard-header">
      <h2>数据概览</h2>
      <el-button @click="refreshData" :loading="tradingStore.loading" type="primary" size="default">
        <el-icon><Refresh /></el-icon>
        刷新数据
      </el-button>
    </div>

    <!-- 第一行: 今日积分进度卡片 -->
    <el-row :gutter="20" class="dashboard-row">
      <el-col :xs="24" :sm="24" :md="24" :lg="24">
        <el-card shadow="hover" class="points-card">
          <template #header>
            <div class="card-header">
              <el-icon color="#409eff"><TrendCharts /></el-icon>
              <span>今日积分进度</span>
            </div>
          </template>
          <div class="points-content">
            <div class="points-numbers">
              <div class="current-points">
                <span class="label">当前积分</span>
                <span class="value">{{ tradingStore.pointsData.current }}</span>
              </div>
              <div class="divider">/</div>
              <div class="target-points">
                <span class="label">目标积分</span>
                <span class="value">{{ tradingStore.pointsData.target }}</span>
              </div>
            </div>
            <el-progress
              :percentage="tradingStore.pointsData.percentage"
              :stroke-width="20"
              :color="getProgressColor(tradingStore.pointsData.percentage)"
              striped
              striped-flow
            >
              <span class="progress-text">{{ tradingStore.pointsData.percentage.toFixed(1) }}%</span>
            </el-progress>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 第二行: 今日交易统计 + 系统运行状态 -->
    <el-row :gutter="20" class="dashboard-row">
      <el-col :xs="24" :sm="24" :md="12" :lg="12">
        <el-card shadow="hover" class="trading-stats-card">
          <template #header>
            <div class="card-header">
              <el-icon color="#67c23a"><DataLine /></el-icon>
              <span>今日交易统计</span>
            </div>
          </template>
          <el-descriptions :column="1" size="large" border>
            <el-descriptions-item>
              <template #label>
                <div class="desc-label">
                  <el-icon><Money /></el-icon>
                  <span>交易额</span>
                </div>
              </template>
              <span class="desc-value primary">{{ formatNumber(tradingStore.tradingStats.volume) }} USDT</span>
            </el-descriptions-item>
            <el-descriptions-item>
              <template #label>
                <div class="desc-label">
                  <el-icon><Files /></el-icon>
                  <span>交易次数</span>
                </div>
              </template>
              <span class="desc-value">{{ tradingStore.tradingStats.count }} 次</span>
            </el-descriptions-item>
            <el-descriptions-item>
              <template #label>
                <div class="desc-label">
                  <el-icon><Coin /></el-icon>
                  <span>磨损金额</span>
                </div>
              </template>
              <span class="desc-value warning">{{ formatNumber(tradingStore.tradingStats.cost) }} USDT</span>
            </el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="24" :md="12" :lg="12">
        <el-card shadow="hover" class="system-status-card">
          <template #header>
            <div class="card-header">
              <el-icon color="#e6a23c"><Monitor /></el-icon>
              <span>系统运行状态</span>
            </div>
          </template>
          <el-descriptions :column="1" size="large" border>
            <el-descriptions-item>
              <template #label>
                <div class="desc-label">
                  <el-icon><Setting /></el-icon>
                  <span>运行模式</span>
                </div>
              </template>
              <el-tag :type="tradingStore.systemStatusType" size="large">
                {{ tradingStore.systemStatusText }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item>
              <template #label>
                <div class="desc-label">
                  <el-icon><Timer /></el-icon>
                  <span>运行时长</span>
                </div>
              </template>
              <span class="desc-value">{{ tradingStore.formatUptime }}</span>
            </el-descriptions-item>
            <el-descriptions-item>
              <template #label>
                <div class="desc-label">
                  <el-icon><Clock /></el-icon>
                  <span>最后操作</span>
                </div>
              </template>
              <span class="desc-value">{{ tradingStore.systemStatus.lastOperation }}</span>
            </el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-col>
    </el-row>

    <!-- 第三行: 资金概览 + 实时盘口 -->
    <el-row :gutter="20" class="dashboard-row">
      <el-col :xs="24" :sm="24" :md="12" :lg="12">
        <el-card shadow="hover" class="funds-card">
          <template #header>
            <div class="card-header">
              <el-icon color="#f56c6c"><Wallet /></el-icon>
              <span>资金概览</span>
            </div>
          </template>
          <el-descriptions :column="1" size="large" border>
            <el-descriptions-item>
              <template #label>
                <div class="desc-label">
                  <el-icon><Money /></el-icon>
                  <span>可用资金</span>
                </div>
              </template>
              <span class="desc-value success">{{ formatNumber(tradingStore.fundsOverview.available) }} USDT</span>
            </el-descriptions-item>
            <el-descriptions-item>
              <template #label>
                <div class="desc-label">
                  <el-icon><TrendCharts /></el-icon>
                  <span>持仓价值</span>
                </div>
              </template>
              <span class="desc-value">{{ formatNumber(tradingStore.fundsOverview.position) }} USDT</span>
            </el-descriptions-item>
            <el-descriptions-item>
              <template #label>
                <div class="desc-label">
                  <el-icon><Grid /></el-icon>
                  <span>网格投入</span>
                </div>
              </template>
              <span class="desc-value">{{ formatNumber(tradingStore.fundsOverview.grid) }} USDT</span>
            </el-descriptions-item>
            <el-descriptions-item>
              <template #label>
                <div class="desc-label">
                  <el-icon><Coin /></el-icon>
                  <span>总资产</span>
                </div>
              </template>
              <span class="desc-value primary bold">{{ formatNumber(tradingStore.totalAssets) }} USDT</span>
            </el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="24" :md="12" :lg="12">
        <el-card shadow="hover" class="market-card">
          <template #header>
            <div class="card-header">
              <el-icon color="#909399"><DataAnalysis /></el-icon>
              <span>实时盘口</span>
            </div>
          </template>
          <el-descriptions :column="1" size="large" border>
            <el-descriptions-item>
              <template #label>
                <div class="desc-label">
                  <el-icon><Top /></el-icon>
                  <span>买一价</span>
                </div>
              </template>
              <span class="desc-value success">{{ formatPrice(tradingStore.marketData.bidPrice) }}</span>
            </el-descriptions-item>
            <el-descriptions-item>
              <template #label>
                <div class="desc-label">
                  <el-icon><Bottom /></el-icon>
                  <span>卖一价</span>
                </div>
              </template>
              <span class="desc-value danger">{{ formatPrice(tradingStore.marketData.askPrice) }}</span>
            </el-descriptions-item>
            <el-descriptions-item>
              <template #label>
                <div class="desc-label">
                  <el-icon><Switch /></el-icon>
                  <span>价差</span>
                </div>
              </template>
              <span class="desc-value">{{ formatPrice(tradingStore.marketData.spread) }}</span>
            </el-descriptions-item>
            <el-descriptions-item>
              <template #label>
                <div class="desc-label">
                  <el-icon><Histogram /></el-icon>
                  <span>ATR值</span>
                </div>
              </template>
              <span class="desc-value">{{ formatPrice(tradingStore.marketData.atr) }}</span>
            </el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useTradingStore } from '@/stores/trading'
import {
  TrendCharts,
  DataLine,
  Monitor,
  Wallet,
  DataAnalysis,
  Money,
  Files,
  Coin,
  Setting,
  Timer,
  Clock,
  Grid,
  Top,
  Bottom,
  Switch,
  Histogram,
  Refresh
} from '@element-plus/icons-vue'

const tradingStore = useTradingStore()

// 格式化数字
const formatNumber = (num: number): string => {
  return num.toLocaleString('zh-CN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })
}

// 格式化价格（更多小数位）
const formatPrice = (num: number): string => {
  return num.toLocaleString('zh-CN', {
    minimumFractionDigits: 5,
    maximumFractionDigits: 5
  })
}

// 根据进度返回颜色
const getProgressColor = (percentage: number) => {
  if (percentage < 30) return '#f56c6c'
  if (percentage < 70) return '#e6a23c'
  return '#67c23a'
}

// 刷新数据
const refreshData = () => {
  tradingStore.loadMockData()
}

// 组件挂载时加载数据
onMounted(() => {
  tradingStore.loadMockData()
})
</script>

<style scoped lang="scss">
.dashboard {
  padding: 20px;

  .dashboard-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;

    h2 {
      margin: 0;
      font-size: 24px;
      font-weight: 600;
      color: #303133;
    }
  }

  .dashboard-row {
    margin-bottom: 20px;

    &:last-child {
      margin-bottom: 0;
    }
  }

  .card-header {
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 600;
    font-size: 16px;
  }

  // 积分卡片样式
  .points-card {
    .points-content {
      .points-numbers {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 20px;
        margin-bottom: 30px;

        .current-points,
        .target-points {
          display: flex;
          flex-direction: column;
          align-items: center;

          .label {
            font-size: 14px;
            color: #909399;
            margin-bottom: 8px;
          }

          .value {
            font-size: 36px;
            font-weight: 700;
            color: #303133;
          }
        }

        .current-points .value {
          color: #409eff;
        }

        .divider {
          font-size: 36px;
          font-weight: 300;
          color: #dcdfe6;
        }
      }

      .el-progress {
        :deep(.el-progress__text) {
          font-size: 16px !important;
          font-weight: 600;
        }
      }

      .progress-text {
        font-size: 16px;
        font-weight: 600;
      }
    }
  }

  // 描述列表通用样式
  .el-descriptions {
    :deep(.el-descriptions__label) {
      width: 35%;
      background-color: #fafafa;
    }

    .desc-label {
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .desc-value {
      font-size: 16px;
      font-weight: 500;

      &.primary {
        color: #409eff;
      }

      &.success {
        color: #67c23a;
      }

      &.warning {
        color: #e6a23c;
      }

      &.danger {
        color: #f56c6c;
      }

      &.bold {
        font-weight: 700;
        font-size: 18px;
      }
    }
  }

  // 响应式布局
  @media (max-width: 768px) {
    padding: 10px;

    .dashboard-header {
      flex-direction: column;
      gap: 10px;
      align-items: flex-start;

      h2 {
        font-size: 20px;
      }
    }

    .dashboard-row {
      margin-bottom: 10px;
    }

    .points-content {
      .points-numbers {
        gap: 10px !important;

        .current-points,
        .target-points {
          .value {
            font-size: 24px !important;
          }
        }

        .divider {
          font-size: 24px !important;
        }
      }
    }

    .el-descriptions {
      :deep(.el-descriptions__label) {
        width: 40%;
      }

      .desc-value {
        font-size: 14px;

        &.bold {
          font-size: 16px;
        }
      }
    }
  }
}
</style>
