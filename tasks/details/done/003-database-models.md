# #003 设计数据库模型

## 📋 元信息

| 项目 | 内容 |
|------|------|
| **任务编号** | #003 |
| **状态** | DONE |
| **负责人** | @Claude |
| **优先级** | 高🔴 |
| **预计工时** | 3小时 |
| **实际工时** | 2.5小时 |
| **标签** | `backend`, `database`, `sqlalchemy` |
| **依赖任务** | #001 |
| **创建时间** | 2025-11-27 11:00 |
| **开始时间** | 2025-11-28 |
| **完成时间** | 2025-11-28 |

---

## 🎯 任务目标

设计并实现完整的数据库模型，包括用户、配置、交易记录、市场数据等核心表结构。

**背景**：
根据系统设计文档第4.1节，需要设计8个核心表。使用SQLAlchemy ORM + SQLite数据库。

**目标**：
- 设计所有核心数据表
- 实现SQLAlchemy模型
- 创建数据库初始化脚本
- 编写数据库迁移工具

---

## 📝 详细描述

### 需要完成的工作

1. **创建数据库模型文件**
   ```
   backend/models/
   ├── __init__.py
   ├── database.py          # 数据库连接配置
   ├── base.py              # Base模型
   ├── user.py              # 用户表
   ├── config.py            # 配置表
   ├── trade.py             # 交易记录表
   ├── market_data.py       # 市场数据表
   ├── orderbook.py         # 盘口快照表
   ├── points_history.py    # 积分历史表
   ├── grid_trade.py        # 网格交易表
   └── system_log.py        # 系统日志表
   ```

2. **核心表设计**（参考系统设计文档4.1节）

   **users 用户表**
   ```python
   - id (主键)
   - username (唯一索引)
   - password_hash
   - created_at
   - last_login
   ```

   **config 配置表**（KV存储）
   ```python
   - id
   - key (唯一索引)
   - value (JSON)
   - updated_at
   ```

   **trades 交易记录表**
   ```python
   - id
   - symbol (索引)
   - side (buy/sell)
   - price (DECIMAL)
   - quantity (DECIMAL)
   - cost (手续费)
   - order_id
   - status
   - created_at (索引)
   ```

   **market_data 市场数据表**（OHLCV + ATR）
   ```python
   - id
   - symbol (索引)
   - timestamp (索引)
   - open, high, low, close (DECIMAL)
   - volume
   - atr
   ```

   **orderbook_snapshots 盘口快照表**
   ```python
   - id
   - symbol
   - timestamp (索引)
   - bids (JSON)
   - asks (JSON)
   ```

   **points_history 积分历史表**
   ```python
   - id
   - date (唯一索引)
   - base_points
   - trade_points
   - total_points
   - balance
   - volume
   ```

   **grid_trades 网格交易表**
   ```python
   - id
   - grid_id
   - symbol
   - side
   - price
   - quantity
   - status
   - created_at
   ```

   **system_logs 系统日志表**
   ```python
   - id
   - level (INFO/WARNING/ERROR)
   - module
   - message
   - extra_data (JSON)
   - created_at (索引)
   ```

3. **实现数据库连接管理**
   - 使用 aiosqlite（异步SQLite）
   - 配置连接池
   - 实现上下文管理器

4. **创建数据库初始化脚本**
   ```python
   # backend/scripts/init_db.py
   - 创建所有表
   - 创建初始管理员用户
   - 插入默认配置
   ```

5. **实现基础CRUD工具**
   - Base模型类（包含通用方法）
   - 查询助手函数
   - 事务管理

### 技术要点
- 使用 SQLAlchemy 2.0+ 语法
- 价格和数量字段使用 DECIMAL 类型（高精度）
- 时间字段使用 TIMESTAMP
- 合理使用索引（提升查询性能）
- JSON字段用于存储复杂数据

### 实现建议
- 参考 FastAPI 官方数据库教程
- 使用 Alembic 进行数据库迁移（可选，初期可手动管理）
- 所有模型继承自 Base 类
- 实现 `__repr__` 方法方便调试

---

## ✅ 验收标准

- [ ] 所有8个核心表的模型文件已创建
- [ ] database.py 实现数据库连接和会话管理
- [ ] base.py 实现Base模型和通用方法
- [ ] 所有模型包含必要的字段和索引
- [ ] 价格字段使用DECIMAL类型
- [ ] 初始化脚本可以成功创建数据库
- [ ] 运行初始化脚本后 data/alpha-score.db 文件存在
- [ ] 可以成功插入和查询测试数据
- [ ] 代码包含类型注解和文档字符串
- [ ] 通过 SQLAlchemy 的表结构验证

---

## 📁 相关文件

需要创建的文件：
- `backend/models/database.py` - 数据库连接
- `backend/models/base.py` - Base模型
- `backend/models/user.py` - 用户模型
- `backend/models/config.py` - 配置模型
- `backend/models/trade.py` - 交易模型
- `backend/models/market_data.py` - 市场数据模型
- `backend/models/orderbook.py` - 盘口模型
- `backend/models/points_history.py` - 积分历史模型
- `backend/models/grid_trade.py` - 网格交易模型
- `backend/models/system_log.py` - 系统日志模型
- `backend/scripts/init_db.py` - 数据库初始化脚本

---

## 📚 参考资料

- [系统设计文档](../../docs/system_design.md) - 第4.1节数据模型设计
- [SQLAlchemy 2.0文档](https://docs.sqlalchemy.org/en/20/)
- [FastAPI数据库教程](https://fastapi.tiangolo.com/tutorial/sql-databases/)
- [aiosqlite文档](https://aiosqlite.omnilib.dev/)

---

## 🔗 依赖关系

### 前置任务
- #001 初始化后端FastAPI项目 - 需要基础项目结构

### 后续任务
- #004 实现用户认证API - 需要user模型
- #013 实现数据采集模块 - 需要market_data和orderbook模型
- 所有后端功能 - 都依赖数据库模型

### 并行任务
- #002 初始化前端Vue3项目 - 可以并行开发

---

## 💬 协作说明

**输出物**：
- 完整的数据库模型代码
- 数据库初始化脚本
- 可以直接被其他模块导入使用

**接口约定**：
- 所有模型使用统一的Base类
- 使用async/await异步查询
- 时间字段统一使用UTC时间

---

## 📝 开发日志

### 2025-11-28 - 任务完成
- ✅ 创建了 database.py 数据库连接配置文件
- ✅ 创建了 base.py 基础模型类（TimestampMixin）
- ✅ 实现了 8 个核心数据模型：
  - user.py - 用户模型
  - config.py - 配置模型
  - trade.py - 交易记录模型
  - market_data.py - 市场数据模型
  - orderbook.py - 盘口快照模型
  - points_history.py - 积分历史模型
  - grid_trade.py - 网格交易模型
  - system_log.py - 系统日志模型
- ✅ 创建了数据库初始化脚本 init_db.py
- ✅ 测试通过：成功创建数据库和初始数据
- ✅ 数据库文件：data/alpha-score.db (180KB)
- ✅ 初始数据：1个管理员用户，8个默认配置

### 技术决策
- 使用 SQLAlchemy 2.0+ 异步 API
- 使用 aiosqlite 作为异步 SQLite 驱动
- 价格和数量字段使用整数存储（单位：聪 satoshi）
- 使用 Mapped[] 类型注解
- 使用 declared_attr 创建 mixin 类
- 使用 bcrypt 直接加密密码（避免 passlib 兼容性问题）

---

## ⚠️ 注意事项

- SQLite不支持真正的DECIMAL类型，需要使用字符串或整数存储（建议用整数存储，单位为最小精度）
- 价格可以存储为整数（单位：聪satoshi），需要时转换为浮点数
- JSON字段在SQLite中存储为TEXT，查询时需要注意
- 确保所有表都有created_at或timestamp字段
- 敏感数据（如密码）必须加密存储
- 索引不要过多，影响写入性能

---

## 🏁 完成检查清单

- [x] 所有验收标准已满足
- [x] 数据库文件可以成功创建
- [x] 测试数据插入和查询成功
- [x] 代码已提交并推送
- [x] TASKS.md已更新状态
- [x] 此文件已移动到 `tasks/details/done/`
- [x] 已通知#004任务可以开始

---

**最后更新**: 2025-11-28 23:20 | **更新人**: @Claude | **状态**: DONE
