<template>
  <div class="ladder-designer">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <div class="title">
            <el-icon><Grid /></el-icon>
            <span>{{ title }}</span>
          </div>
          <el-space>
            <el-button @click="addLadder" type="primary" size="small">
              <el-icon><Plus /></el-icon>
              添加阶梯
            </el-button>
            <el-button @click="resetLadders" size="small">
              <el-icon><RefreshLeft /></el-icon>
              重置
            </el-button>
          </el-space>
        </div>
      </template>

      <!-- 阶梯表格 -->
      <el-table :data="ladders" border stripe style="width: 100%">
        <el-table-column label="序号" width="80" align="center">
          <template #default="{ $index }">
            {{ $index + 1 }}
          </template>
        </el-table-column>

        <el-table-column label="起始值" width="150">
          <template #default="{ row }">
            <el-input-number
              v-model="row.range[0]"
              :min="0"
              :precision="2"
              :controls="false"
              size="small"
              style="width: 100%"
              @change="validateLadders"
            />
          </template>
        </el-table-column>

        <el-table-column label="结束值" width="150">
          <template #default="{ row }">
            <el-input-number
              v-model="row.range[1]"
              :min="0"
              :precision="2"
              :controls="false"
              size="small"
              style="width: 100%"
              placeholder="留空表示无上限"
              @change="validateLadders"
            />
          </template>
        </el-table-column>

        <el-table-column label="积分值" width="150">
          <template #default="{ row }">
            <el-input-number
              v-model="row.points"
              :min="0"
              :precision="1"
              :controls="false"
              size="small"
              style="width: 100%"
            />
          </template>
        </el-table-column>

        <el-table-column label="范围描述" min-width="200">
          <template #default="{ row }">
            <span class="range-desc">
              {{ formatRangeDescription(row.range) }}
            </span>
          </template>
        </el-table-column>

        <el-table-column label="操作" width="120" align="center" fixed="right">
          <template #default="{ $index }">
            <el-button
              @click="moveLadderUp($index)"
              :disabled="$index === 0"
              type="text"
              size="small"
            >
              <el-icon><Top /></el-icon>
            </el-button>
            <el-button
              @click="moveLadderDown($index)"
              :disabled="$index === ladders.length - 1"
              type="text"
              size="small"
            >
              <el-icon><Bottom /></el-icon>
            </el-button>
            <el-button @click="removeLadder($index)" type="text" size="small" danger>
              <el-icon><Delete /></el-icon>
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 验证提示 -->
      <div v-if="validationErrors.length > 0" class="validation-errors">
        <el-alert
          v-for="(error, index) in validationErrors"
          :key="index"
          :title="error"
          type="error"
          :closable="false"
          show-icon
        />
      </div>

      <!-- 可视化预览 -->
      <div class="ladder-preview">
        <h4>阶梯可视化预览</h4>
        <div class="preview-container">
          <div
            v-for="(ladder, index) in ladders"
            :key="index"
            class="ladder-item"
            :style="{ width: getLadderWidth(ladder) + '%' }"
          >
            <div class="ladder-label">
              {{ formatRangeDescription(ladder.range) }}
            </div>
            <div class="ladder-points">{{ ladder.points }} 分</div>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { Grid, Plus, RefreshLeft, Top, Bottom, Delete } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

// 阶梯类型定义
export interface Ladder {
  range: [number, number | null]
  points: number
}

// Props
const props = defineProps<{
  title: string
  modelValue: Ladder[]
  valueUnit?: string // 值的单位（如USDT）
}>()

// Emits
const emit = defineEmits<{
  (e: 'update:modelValue', value: Ladder[]): void
}>()

// 阶梯数据
const ladders = ref<Ladder[]>([...props.modelValue])

// 验证错误
const validationErrors = ref<string[]>([])

// 监听父组件传入的值变化
watch(
  () => props.modelValue,
  (newValue) => {
    ladders.value = [...newValue]
  },
  { deep: true }
)

// 监听阶梯变化，通知父组件
watch(
  ladders,
  (newValue) => {
    emit('update:modelValue', newValue)
    validateLadders()
  },
  { deep: true }
)

// 添加阶梯
const addLadder = () => {
  const lastLadder = ladders.value[ladders.value.length - 1]
  const start = lastLadder ? (lastLadder.range[1] || lastLadder.range[0] + 1000) : 0

  ladders.value.push({
    range: [start, start + 1000],
    points: 1.0
  })

  ElMessage.success('已添加新阶梯')
}

// 删除阶梯
const removeLadder = (index: number) => {
  if (ladders.value.length <= 1) {
    ElMessage.warning('至少需要保留一个阶梯')
    return
  }

  ladders.value.splice(index, 1)
  ElMessage.success('已删除阶梯')
}

// 上移阶梯
const moveLadderUp = (index: number) => {
  if (index === 0) return

  const temp = ladders.value[index]
  ladders.value[index] = ladders.value[index - 1]
  ladders.value[index - 1] = temp
}

// 下移阶梯
const moveLadderDown = (index: number) => {
  if (index === ladders.value.length - 1) return

  const temp = ladders.value[index]
  ladders.value[index] = ladders.value[index + 1]
  ladders.value[index + 1] = temp
}

// 重置阶梯
const resetLadders = () => {
  ladders.value = [...props.modelValue]
  ElMessage.info('已重置为初始值')
}

// 验证阶梯配置
const validateLadders = () => {
  validationErrors.value = []

  for (let i = 0; i < ladders.value.length; i++) {
    const ladder = ladders.value[i]

    // 验证范围有效性
    if (ladder.range[1] !== null && ladder.range[0] >= ladder.range[1]) {
      validationErrors.value.push(`阶梯${i + 1}: 起始值必须小于结束值`)
    }

    // 验证范围连续性
    if (i > 0) {
      const prevLadder = ladders.value[i - 1]
      if (prevLadder.range[1] !== null && ladder.range[0] !== prevLadder.range[1]) {
        validationErrors.value.push(
          `阶梯${i + 1}: 起始值应该等于上一阶梯的结束值 (${prevLadder.range[1]})`
        )
      }
    }

    // 验证积分值
    if (ladder.points < 0) {
      validationErrors.value.push(`阶梯${i + 1}: 积分值不能为负数`)
    }
  }
}

// 格式化范围描述
const formatRangeDescription = (range: [number, number | null]) => {
  const unit = props.valueUnit || ''
  if (range[1] === null) {
    return `≥ ${range[0].toFixed(2)} ${unit}`
  }
  return `${range[0].toFixed(2)} - ${range[1].toFixed(2)} ${unit}`
}

// 计算阶梯宽度（用于可视化）
const getLadderWidth = (ladder: Ladder) => {
  const totalRange = ladders.value.reduce((sum, l) => {
    const width = l.range[1] === null ? 1000 : l.range[1] - l.range[0]
    return sum + width
  }, 0)

  const currentWidth = ladder.range[1] === null ? 1000 : ladder.range[1] - ladder.range[0]
  return (currentWidth / totalRange) * 100
}

// 初始验证
validateLadders()
</script>

<style scoped lang="scss">
.ladder-designer {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    .title {
      display: flex;
      align-items: center;
      gap: 8px;
      font-weight: bold;
      font-size: 16px;
    }
  }

  .range-desc {
    font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
    font-size: 13px;
  }

  .validation-errors {
    margin-top: 20px;

    .el-alert {
      margin-bottom: 10px;
    }
  }

  .ladder-preview {
    margin-top: 30px;
    padding-top: 20px;
    border-top: 1px solid #ebeef5;

    h4 {
      margin-bottom: 15px;
      font-size: 14px;
      color: #606266;
    }

    .preview-container {
      display: flex;
      height: 80px;
      border: 1px solid #dcdfe6;
      border-radius: 4px;
      overflow: hidden;

      .ladder-item {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        border-right: 1px solid #dcdfe6;
        background: linear-gradient(to right, #409eff, #67c23a);
        color: white;
        font-size: 12px;
        padding: 5px;
        transition: all 0.3s;

        &:last-child {
          border-right: none;
        }

        &:hover {
          transform: scale(1.05);
          z-index: 1;
          box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
        }

        .ladder-label {
          font-weight: 600;
          margin-bottom: 5px;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
          max-width: 100%;
        }

        .ladder-points {
          font-size: 16px;
          font-weight: bold;
        }
      }
    }
  }
}
</style>
