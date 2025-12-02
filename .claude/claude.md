# Claude AI 开发助手配置

## 项目概述
Binance Alpha 自动化交易工具 - 用于自动化获取 Alpha 积分和网格交易

## 开发原则
1. 隐蔽性优先：所有操作必须模拟人类行为
2. 安全第一：严格风控,保护用户资金
3. 模块化设计：高内聚、低耦合
4. 配置化：所有参数可配置

## 技术栈
- 后端：Python 3.11+ / FastAPI / Playwright / SQLite
- 前端：Vue 3 / TypeScript / Vite / Element Plus
- OSD：PyQt6
- **代理/部署**：
  - 开发环境：Vite Proxy（已配置在vite.config.ts）
  - 生产环境：Caddy（自动HTTPS，配置简单）

## 部署架构

### 开发环境
```
[客户端] → [Vite Dev Server :5173] → [Vite Proxy] → [FastAPI :8000]
         ↓ 静态资源
         [Vue 3 SPA]
```

### 生产环境
```
[客户端] → [Caddy :80/:443] → [FastAPI :8000]
         ↓ 静态资源        ↓ API请求
         [Vue Dist]        [后端服务]
```

### 配置位置
- 开发代理：`frontend/vite.config.ts` - server.proxy配置
- 生产反向代理：`Caddyfile`（待创建）
- 环境变量：`frontend/.env` (开发) / `.env.production` (生产)

## 代码规范
- Python：PEP 8 + Type Hints + Black
- TypeScript：ESLint + Prettier + Strict Mode

## 常用命令
- 启动后端：`cd backend && uvicorn main:app --reload`
- 启动前端：`cd frontend && npm run dev`
- 运行测试：`pytest tests/`

## 注意事项
- 所有浏览器操作必须包含行为模拟（随机延迟、鼠标移动）
- 配置变更后需验证合法性
- 关键操作需记录日志
- 异常情况需发送通知

## 📊 会话管理规范

### 上下文监控
- **监控阈值**: 当上下文使用达到 **90%** 时，必须主动提醒用户
- **任务完成汇报**: 每个任务完成后，必须显示当前上下文使用情况
  - 格式：`已使用Token: X / 200,000 (XX.X%)`
  - 示例：`已使用Token: 53,264 / 200,000 (26.6%)`
- **提醒内容**:
  - 当前token使用量和百分比
  - 建议用户总结关键信息或开始新会话
  - 提供当前会话的重要成果摘要
- **日常检查**: 在执行大型任务前检查剩余上下文是否充足
- **优化建议**:
  - 定期清理不需要的后台进程
  - 避免重复读取大文件
  - 及时总结和归档已完成的任务信息

### 后台进程管理
- 定期检查和清理已完成或失败的后台bash进程
- 长时间运行的进程应当有明确的监控和终止条件

---

## 🚨 任务管理规范（强制遵守）

### 核心原则
本项目使用**任务看板系统**进行多AI Agent协作开发。所有AI Agent（Claude、Cursor、Kiro、Windsurf等）必须严格遵守以下规范。

### 📋 任务文件位置
- **主看板**: `TASKS.md` - 全局任务列表和状态概览
- **任务详情**: `tasks/details/{todo,doing,done,blocked}/` - 详细任务描述文件
- **任务模板**: `tasks/TASK_TEMPLATE.md` - 创建新任务的模板

### 🔴 强制规则（违反将导致任务无效）

#### 1. 工作前必读
```bash
# 每次开始工作前必须执行
git pull origin main
cat TASKS.md  # 查看最新任务状态
```

#### 2. 认领任务流程（必须按顺序执行）
```bash
# Step 1: 确保本地最新
git pull origin main

# Step 2: 编辑TASKS.md认领任务
# 将 @无人认领 改为 @你的名字（如 @Claude）
# 更新"Agent工作分配"表格

# Step 3: 立即提交（避免冲突）
git add TASKS.md
git commit -m "task: 认领任务 #001"
git push origin main
```

#### 3. 开始任务流程
```bash
# Step 1: 移动任务到DOING区域
# 在TASKS.md中将任务从TODO移到DOING

# Step 2: 移动详情文件
mv tasks/details/todo/001-*.md tasks/details/doing/

# Step 3: 添加开始时间
# 在任务中添加 `开始:2025-11-27 10:00`

# Step 4: 提交变更
git add TASKS.md tasks/
git commit -m "task: 开始任务 #001"
git push origin main
```

#### 4. 完成任务流程
```bash
# Step 1: 更新TASKS.md
# - 将 [ ] 改为 [x]
# - 移动到DONE区域
# - 添加完成时间和实际工时

# Step 2: 移动详情文件
mv tasks/details/doing/001-*.md tasks/details/done/

# Step 3: 更新详情文件
# - 勾选所有验收标准
# - 填写实际工时
# - 完成开发日志

# Step 4: 提交所有变更
git add TASKS.md tasks/ <相关代码文件>
git commit -m "task: 完成任务 #001 初始化后端FastAPI项目"
git push origin main
```

#### 5. 遇到阻塞时
```bash
# Step 1: 移动任务到BLOCKED区域
# Step 2: 添加阻塞原因说明
# Step 3: 立即提交并通知Human
git add TASKS.md
git commit -m "task: 阻塞任务 #001 - 原因说明"
git push origin main
```

### ⚠️ 禁止行为
- ❌ 不执行git pull直接修改TASKS.md
- ❌ 同时认领多个任务（除非明确许可）
- ❌ 修改其他Agent已认领的任务
- ❌ 完成任务后不更新TASKS.md
- ❌ 跳过任务详情文件直接开发
- ❌ 不检查依赖关系就开始任务

### ✅ 推荐做法
- ✅ 认领任务前先阅读详情文件
- ✅ 开发过程中及时更新开发日志
- ✅ 遇到问题立即在详情文件中记录
- ✅ 完成后检查所有验收标准
- ✅ 提交时使用规范的commit message

### 📝 Commit Message格式
```
task: <操作> #<编号> <简短描述>

示例:
task: 认领 #001 后端初始化
task: 开始 #001 后端初始化
task: 更新 #001 添加依赖安装步骤
task: 完成 #001 后端初始化
task: 阻塞 #001 等待数据库模型设计
```

### 🔍 任务状态检查
开发过程中随时可以执行：
```bash
cat TASKS.md | grep "@Claude"  # 查看自己的任务
cat TASKS.md | grep "DOING"    # 查看进行中的任务
```

### 📚 更多信息
详细使用指南请查看：`tasks/README.md`
