<template>
  <div class="points-calculator">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <el-icon><Operation /></el-icon>
          <span>积分计算模拟器</span>
        </div>
      </template>

      <!-- 输入区域 -->
      <el-form label-width="120px">
        <el-form-item label="账户余额">
          <el-input-number
            v-model="balance"
            :min="0"
            :precision="2"
            :controls="true"
            style="width: 200px"
            @change="calculate"
          />
          <span class="unit">USDT</span>
        </el-form-item>

        <el-form-item label="每日交易量">
          <el-input-number
            v-model="dailyVolume"
            :min="0"
            :precision="2"
            :controls="true"
            style="width: 200px"
            @change="calculate"
          />
          <span class="unit">USDT</span>
        </el-form-item>
      </el-form>

      <!-- 计算结果 -->
      <el-divider />

      <div class="result-section">
        <h4>计算结果</h4>

        <el-row :gutter="20">
          <el-col :xs="24" :sm="12" :md="8">
            <el-statistic title="资金阶梯积分" :value="result.balancePoints" suffix="分">
              <template #prefix>
                <el-icon color="#409eff"><Trophy /></el-icon>
              </template>
            </el-statistic>
            <div class="statistic-desc">基于账户余额 {{ balance.toFixed(2) }} USDT</div>
          </el-col>

          <el-col :xs="24" :sm="12" :md="8">
            <el-statistic title="交易量积分" :value="result.volumePoints" suffix="分">
              <template #prefix>
                <el-icon color="#67c23a"><Coin /></el-icon>
              </template>
            </el-statistic>
            <div class="statistic-desc">基于每日交易量 {{ dailyVolume.toFixed(2) }} USDT</div>
          </el-col>

          <el-col :xs="24" :sm="12" :md="8">
            <el-statistic title="总计" :value="result.totalPoints" suffix="分">
              <template #prefix>
                <el-icon color="#f56c6c"><Star /></el-icon>
              </template>
            </el-statistic>
            <div class="statistic-desc total">每日可获得总积分</div>
          </el-col>
        </el-row>
      </div>

      <!-- 阶梯匹配详情 -->
      <el-divider />

      <div class="ladder-match">
        <h4>阶梯匹配详情</h4>

        <el-descriptions :column="1" border>
          <el-descriptions-item label="资金阶梯">
            <el-tag type="info">{{ result.balanceLadderDesc }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="交易量阶梯">
            <el-tag type="success">{{ result.volumeLadderDesc }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="下一阶梯">
            <div v-if="result.nextBalanceLadder">
              资金达到 <strong>{{ result.nextBalanceLadder }} USDT</strong> 可升级，将获得更多积分
            </div>
            <div v-if="result.nextVolumeLadder">
              交易量达到 <strong>{{ result.nextVolumeLadder }} USDT</strong> 可升级，将获得更多积分
            </div>
            <div v-if="!result.nextBalanceLadder && !result.nextVolumeLadder">
              <el-tag type="warning">已达到最高阶梯</el-tag>
            </div>
          </el-descriptions-item>
        </el-descriptions>
      </div>

      <!-- 快速预设 -->
      <el-divider />

      <div class="presets">
        <h4>快速预设</h4>
        <el-space wrap>
          <el-button
            v-for="preset in presets"
            :key="preset.label"
            @click="applyPreset(preset)"
            size="small"
          >
            {{ preset.label }}
          </el-button>
        </el-space>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { Operation, Trophy, Coin, Star } from '@element-plus/icons-vue'
import type { Ladder } from './LadderDesigner.vue'

// Props
const props = defineProps<{
  balanceLadders: Ladder[]
  volumeLadders: Ladder[]
}>()

// 输入值
const balance = ref(1000)
const dailyVolume = ref(500)

// 计算结果
const result = reactive({
  balancePoints: 0,
  volumePoints: 0,
  totalPoints: 0,
  balanceLadderDesc: '',
  volumeLadderDesc: '',
  nextBalanceLadder: null as number | null,
  nextVolumeLadder: null as number | null
})

// 快速预设
const presets = [
  { label: '新手 (500/200)', balance: 500, volume: 200 },
  { label: '进阶 (2000/1000)', balance: 2000, volume: 1000 },
  { label: '高级 (5000/3000)', balance: 5000, volume: 3000 },
  { label: '专业 (10000/5000)', balance: 10000, volume: 5000 }
]

// 查找匹配的阶梯
const findMatchingLadder = (value: number, ladders: Ladder[]) => {
  for (let i = 0; i < ladders.length; i++) {
    const ladder = ladders[i]
    if (value >= ladder.range[0]) {
      if (ladder.range[1] === null || value < ladder.range[1]) {
        return {
          ladder,
          index: i,
          points: ladder.points,
          nextLadder: i < ladders.length - 1 ? ladders[i + 1] : null
        }
      }
    }
  }
  return null
}

// 格式化阶梯描述
const formatLadderRange = (range: [number, number | null]) => {
  if (range[1] === null) {
    return `≥ ${range[0].toFixed(0)}`
  }
  return `${range[0].toFixed(0)} - ${range[1].toFixed(0)}`
}

// 计算积分
const calculate = () => {
  // 计算资金阶梯积分
  const balanceMatch = findMatchingLadder(balance.value, props.balanceLadders)
  if (balanceMatch) {
    result.balancePoints = balanceMatch.points
    result.balanceLadderDesc = formatLadderRange(balanceMatch.ladder.range) + ' USDT'
    result.nextBalanceLadder = balanceMatch.nextLadder ? balanceMatch.nextLadder.range[0] : null
  } else {
    result.balancePoints = 0
    result.balanceLadderDesc = '未匹配'
    result.nextBalanceLadder = null
  }

  // 计算交易量阶梯积分
  const volumeMatch = findMatchingLadder(dailyVolume.value, props.volumeLadders)
  if (volumeMatch) {
    result.volumePoints = volumeMatch.points
    result.volumeLadderDesc = formatLadderRange(volumeMatch.ladder.range) + ' USDT'
    result.nextVolumeLadder = volumeMatch.nextLadder ? volumeMatch.nextLadder.range[0] : null
  } else {
    result.volumePoints = 0
    result.volumeLadderDesc = '未匹配'
    result.nextVolumeLadder = null
  }

  // 计算总积分
  result.totalPoints = result.balancePoints + result.volumePoints
}

// 应用预设
const applyPreset = (preset: { balance: number; volume: number }) => {
  balance.value = preset.balance
  dailyVolume.value = preset.volume
  calculate()
}

// 初始化计算
onMounted(() => {
  calculate()
})
</script>

<style scoped lang="scss">
.points-calculator {
  .card-header {
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: bold;
    font-size: 16px;
  }

  .unit {
    margin-left: 10px;
    color: #909399;
  }

  .result-section {
    h4 {
      margin-bottom: 20px;
      font-size: 14px;
      color: #606266;
    }

    .statistic-desc {
      margin-top: 8px;
      font-size: 12px;
      color: #909399;

      &.total {
        color: #f56c6c;
        font-weight: 600;
      }
    }
  }

  .ladder-match {
    h4 {
      margin-bottom: 15px;
      font-size: 14px;
      color: #606266;
    }

    strong {
      color: #409eff;
      font-weight: 600;
    }
  }

  .presets {
    h4 {
      margin-bottom: 15px;
      font-size: 14px;
      color: #606266;
    }
  }

  :deep(.el-statistic__head) {
    font-size: 13px;
    color: #909399;
  }

  :deep(.el-statistic__number) {
    font-size: 28px;
    font-weight: bold;
  }
}
</style>
