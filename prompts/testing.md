# 测试阶段 AI 提示词

## 测试要求

### 单元测试
- 使用 pytest（Python）
- 使用 Vitest（Vue3/TypeScript）
- 覆盖率 > 80%
- 测试关键业务逻辑

### 集成测试
- API 接口测试
- 数据库操作测试
- WebSocket 通信测试
- 浏览器自动化测试

### E2E 测试
- 用户登录流程
- 交易执行流程
- 配置修改流程
- 异常处理流程

## 测试用例示例

### Python 单元测试
```python
import pytest
from backend.modules.strategy.points_calculator import calculate_points

def test_calculate_points():
    """测试积分计算"""
    balance = 2000  # 2000 USDT
    volume = 8000   # 8000 USDT 交易量

    points = calculate_points(balance, volume)

    assert points > 0
    assert isinstance(points, float)
```

### TypeScript 单元测试
```typescript
import { describe, it, expect } from 'vitest'
import { useTradingStore } from '@/stores/trading'

describe('Trading Store', () => {
  it('should update price correctly', () => {
    const store = useTradingStore()
    store.updatePrice(0.005432)
    expect(store.currentPrice).toBe(0.005432)
  })
})
```

## 测试运行命令
- 后端单元测试：`pytest tests/unit/`
- 前端单元测试：`npm run test:unit`
- 集成测试：`pytest tests/integration/`
- E2E 测试：`pytest tests/e2e/`
