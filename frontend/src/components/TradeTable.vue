<template>
  <div class="trade-table">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <el-icon><List /></el-icon>
          <span>实时交易列表</span>
        </div>
      </template>

      <!-- 筛选栏 -->
      <div class="filter-bar">
        <el-space wrap>
          <el-select v-model="filters.side" placeholder="交易方向" clearable style="width: 120px">
            <el-option label="全部" value="" />
            <el-option label="买入" value="buy" />
            <el-option label="卖出" value="sell" />
          </el-select>
          <el-date-picker
            v-model="filters.dateRange"
            type="datetimerange"
            range-separator="至"
            start-placeholder="开始时间"
            end-placeholder="结束时间"
            style="width: 360px"
            clearable
          />
          <el-button @click="handleFilter" type="primary">
            <el-icon><Search /></el-icon>
            筛选
          </el-button>
          <el-button @click="handleReset">
            <el-icon><RefreshLeft /></el-icon>
            重置
          </el-button>
        </el-space>
      </div>

      <!-- 数据表格 -->
      <el-table
        :data="paginatedData"
        v-loading="loading"
        stripe
        border
        style="width: 100%"
        @sort-change="handleSortChange"
      >
        <el-table-column prop="timestamp" label="时间" width="180" sortable="custom">
          <template #default="{ row }">
            {{ formatTime(row.timestamp) }}
          </template>
        </el-table-column>

        <el-table-column prop="side" label="方向" width="80" align="center">
          <template #default="{ row }">
            <el-tag :type="row.side === 'buy' ? 'success' : 'danger'" size="small">
              {{ row.side === 'buy' ? '买入' : '卖出' }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="symbol" label="交易对" width="120" />

        <el-table-column prop="price" label="价格 (USDT)" width="130" align="right" sortable="custom">
          <template #default="{ row }">
            <span :class="row.side === 'buy' ? 'text-success' : 'text-danger'">
              {{ row.price.toFixed(4) }}
            </span>
          </template>
        </el-table-column>

        <el-table-column prop="quantity" label="数量" width="130" align="right" sortable="custom">
          <template #default="{ row }">
            {{ row.quantity.toFixed(6) }}
          </template>
        </el-table-column>

        <el-table-column prop="cost" label="成交额 (USDT)" width="150" align="right" sortable="custom">
          <template #default="{ row }">
            <span class="font-bold">{{ row.cost.toFixed(2) }}</span>
          </template>
        </el-table-column>

        <el-table-column prop="points" label="获得积分" width="100" align="right">
          <template #default="{ row }">
            <span class="text-primary">+{{ row.points }}</span>
          </template>
        </el-table-column>

        <el-table-column prop="status" label="状态" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)" size="small">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column label="备注" min-width="150">
          <template #default="{ row }">
            <span class="text-secondary">{{ row.note || '-' }}</span>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="pagination.currentPage"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="filteredData.length"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { List, Search, RefreshLeft } from '@element-plus/icons-vue'

// 交易记录类型定义
export interface TradeRecord {
  id: string
  timestamp: string
  side: 'buy' | 'sell'
  symbol: string
  price: number
  quantity: number
  cost: number
  points: number
  status: 'success' | 'failed' | 'pending'
  note?: string
}

// Props
const props = defineProps<{
  trades: TradeRecord[]
  loading?: boolean
}>()

// 筛选条件
const filters = ref({
  side: '',
  dateRange: null as [Date, Date] | null
})

// 排序
const sortBy = ref({ prop: 'timestamp', order: 'descending' })

// 分页
const pagination = ref({
  currentPage: 1,
  pageSize: 20
})

// 筛选后的数据
const filteredData = computed(() => {
  let data = [...props.trades]

  // 按方向筛选
  if (filters.value.side) {
    data = data.filter((item) => item.side === filters.value.side)
  }

  // 按时间范围筛选
  if (filters.value.dateRange) {
    const [start, end] = filters.value.dateRange
    data = data.filter((item) => {
      const timestamp = new Date(item.timestamp).getTime()
      return timestamp >= start.getTime() && timestamp <= end.getTime()
    })
  }

  // 排序
  if (sortBy.value.prop) {
    data.sort((a, b) => {
      const aVal = a[sortBy.value.prop as keyof TradeRecord]
      const bVal = b[sortBy.value.prop as keyof TradeRecord]

      if (typeof aVal === 'number' && typeof bVal === 'number') {
        return sortBy.value.order === 'ascending' ? aVal - bVal : bVal - aVal
      }
      if (typeof aVal === 'string' && typeof bVal === 'string') {
        return sortBy.value.order === 'ascending'
          ? aVal.localeCompare(bVal)
          : bVal.localeCompare(aVal)
      }
      return 0
    })
  }

  return data
})

// 分页后的数据
const paginatedData = computed(() => {
  const start = (pagination.value.currentPage - 1) * pagination.value.pageSize
  const end = start + pagination.value.pageSize
  return filteredData.value.slice(start, end)
})

// 监听数据变化，重置到第一页
watch(
  () => filteredData.value.length,
  () => {
    pagination.value.currentPage = 1
  }
)

// 事件处理
const handleFilter = () => {
  pagination.value.currentPage = 1
}

const handleReset = () => {
  filters.value = {
    side: '',
    dateRange: null
  }
  sortBy.value = { prop: 'timestamp', order: 'descending' }
  pagination.value.currentPage = 1
}

const handleSortChange = ({ prop, order }: { prop: string; order: string }) => {
  sortBy.value = { prop, order }
}

const handleSizeChange = (val: number) => {
  pagination.value.pageSize = val
}

const handleCurrentChange = (val: number) => {
  pagination.value.currentPage = val
}

// 工具函数
const formatTime = (timestamp: string) => {
  return new Date(timestamp).toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

const getStatusType = (status: string) => {
  const types: Record<string, any> = {
    success: 'success',
    failed: 'danger',
    pending: 'warning'
  }
  return types[status] || 'info'
}

const getStatusText = (status: string) => {
  const texts: Record<string, string> = {
    success: '成功',
    failed: '失败',
    pending: '处理中'
  }
  return texts[status] || '未知'
}
</script>

<style scoped lang="scss">
.trade-table {
  .card-header {
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: bold;
  }

  .filter-bar {
    margin-bottom: 20px;
  }

  .text-success {
    color: #67c23a;
    font-weight: 600;
  }

  .text-danger {
    color: #f56c6c;
    font-weight: 600;
  }

  .text-primary {
    color: #409eff;
    font-weight: 600;
  }

  .text-secondary {
    color: #909399;
  }

  .font-bold {
    font-weight: 600;
  }

  .pagination-container {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
  }
}
</style>
