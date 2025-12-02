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

## 项目文件结构

```
alpha-score/
├── backend/                    # 后端服务
│   ├── api/                   # API路由
│   │   ├── dependencies.py    # 依赖注入（JWT认证等）
│   │   └── routes/            # 路由模块
│   ├── models/                # 数据模型
│   ├── modules/               # 业务模块（预留）
│   │   ├── behavior/          # 行为模拟
│   │   ├── browser/           # 浏览器自动化
│   │   ├── execution/         # 交易执行
│   │   ├── llm/               # LLM集成
│   │   ├── osd/               # OSD窗口
│   │   ├── risk/              # 风控模块
│   │   └── strategy/          # 策略模块
│   ├── utils/                 # 工具模块
│   ├── scripts/               # 脚本
│   ├── main.py                # FastAPI主应用
│   ├── requirements.txt       # Python依赖
│   └── pytest.ini             # 测试配置
│
├── frontend/                  # 前端应用
│   ├── src/
│   │   ├── api/               # API客户端
│   │   ├── components/        # 通用组件
│   │   ├── layouts/           # 布局组件
│   │   ├── pages/             # 页面组件
│   │   ├── router/            # 路由配置
│   │   ├── stores/            # 状态管理
│   │   ├── types/             # TypeScript类型
│   │   ├── utils/             # 工具函数
│   │   ├── App.vue            # 根组件
│   │   └── main.ts            # 入口文件
│   ├── public/                # 静态资源
│   ├── index.html             # HTML模板
│   ├── package.json           # Node依赖
│   ├── vite.config.ts         # Vite配置
│   └── tsconfig.json          # TypeScript配置
│
├── config/                    # 配置文件
│   ├── settings.yaml          # 应用配置（系统、交易、风控等）
│   ├── ladders.yaml           # 积分阶梯配置
│   ├── secrets.yaml           # 敏感配置（API密钥、JWT密钥）
│   └── secrets.yaml.example   # 敏感配置示例
│
├── deployment/                # 部署配置
│   ├── caddy/                 # Caddy反向代理
│   ├── docker/                # Docker容器化
│   ├── nginx/                 # Nginx反向代理
│   ├── systemd/               # Systemd服务
│   └── README.md              # 部署文档总览
│
├── docs/                      # 文档
│
├── tasks/                     # 任务管理（多Agent协作）
│   ├── details/
│   │   ├── todo/              # 待办任务详情
│   │   ├─ doing/             # 进行中任务详情
│   │   ├── done/              # 完成任务详情
│   │   └── blocked/           # 阻塞任务详情
│   ├── TASK_TEMPLATE.md       # 任务模板
│   └── README.md              # 任务管理指南
│
├── logs/                      # 日志目录（gitignore）
│   ├── app/                   # 应用日志（30天保留）
│   ├── error/                 # 错误日志（60天保留）
│   └── trade/                 # 交易日志（90天保留）
│
├── data/                      # 数据目录（gitignore）
│   └── *.db                   # SQLite数据库
│
├── tests/                     # 测试（预留）
│   ├── unit/                  # 单元测试
│   ├── integration/           # 集成测试
│   └── e2e/                   # 端到端测试
│
└── TASKS.md                   # 任务看板
```

### 重要目录说明

#### 后端 (backend/)
- `api/routes/`: 所有API端点，按功能模块分文件
- `models/`: SQLAlchemy数据模型，每个表一个文件
- `utils/`: 可复用工具（配置、日志、JWT、安全）
- `modules/`: 核心业务逻辑（待实现）

#### 前端 (frontend/)
- `api/`: API调用封装，对应后端路由
- `stores/`: Pinia状态管理，按领域划分
- `pages/`: 页面组件，对应路由
- `layouts/`: 布局组件，包含导航

#### 配置 (config/)
- `settings.yaml`: 公开配置
- `secrets.yaml`: 敏感配置（已gitignore）
- 使用Pydantic验证，支持热重载

#### 部署 (deployment/)
- 支持4种部署方式：Docker、Systemd+Nginx、Systemd+Caddy、手动
- 每种方式都有详细的README文档

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
- **任务完成汇报**: 每个任务完成后，必须显示当前上下文使用情况
  - 格式：`已使用Token: X / 200,000 (XX.X%)`

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
