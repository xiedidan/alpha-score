# Kiro AI 项目配置

## 项目信息
- 项目名称：Binance Alpha 自动化交易工具
- 项目类型：Web 应用 + 自动化脚本
- 主要语言：Python, TypeScript

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
│   ├── api/routes/             # API路由 (auth, config, logs, trades)
│   ├── models/                 # 数据模型 (SQLAlchemy)
│   ├── utils/                  # 工具 (config, logger, jwt, security)
│   ├── modules/                # 业务模块(待实现)
│   └── main.py                 # FastAPI主应用
���── frontend/                   # 前端应用
│   ├── src/
│   │   ├── api/                # API客户端
│   │   ├── pages/              # 页面 (Login, Dashboard)
│   │   ├── stores/             # Pinia状态管理
│   │   ├── router/             # Vue Router
│   │   └── layouts/            # 布局组件
│   └── vite.config.ts          # Vite配置
├── config/                     # 配置文件
│   ├── settings.yaml           # 应用配置
│   ├── ladders.yaml            # 积分配置
│   └── secrets.yaml            # 敏感配置(gitignore)
├── deployment/                 # 部署配置
│   ├── caddy/                  # Caddy反向代理
│   ├── docker/                 # Docker容器化
│   ├── nginx/                  # Nginx反向代理
│   └── systemd/                # Systemd服务
├── tasks/                      # 任务管理
│   ├── details/                # 任务详情
│   └── TASKS.md                # 任务看板
├── logs/                       # 日志(gitignore)
├── data/                       # 数据库(gitignore)
└── docs/                       # 文档
```

### 关键目录
- `backend/api/routes/`: API端点按模块分文件
- `frontend/src/stores/`: Pinia状态管理
- `config/`: YAML配置,Pydantic验证
- `deployment/`: 4种部署��式(Docker/Systemd/Nginx/Caddy)

## 部署架构

### 开发环境
```
[客户端] → [Vite :5173 + Proxy] → [FastAPI :8000]
```
- 使用Vite内置开发服务器和代理
- 配置文件：`frontend/vite.config.ts`
- API请求自动转发到后端

### 生产环境
```
[客户端] → [Caddy :80/:443] → [FastAPI :8000]
```
- 使用Caddy作为反向代理
- 自动HTTPS证书管理
- 配置文件：`Caddyfile`（项目根目录）

## 开发指南
### 模块划分
- 前端：Vue3 单页应用
- 后端：FastAPI 异步服务
- 自动化：Playwright 浏览器控制
- 显示：PyQt6 OSD 窗口

### 关键约束
1. 浏览器操作必须隐蔽（模拟人类）
2. 风控规则严格执行
3. 配置实时生效
4. 异常必须通知

### 编码规范
- 使用类型注解
- 添加详细注释
- 编写单元测试
- 遵循项目规范

## 📊 会话管理规范

### 上下文监控
- **监控阈值**: 当上下文使用达到 **90%** 时，必须主动提醒用户
- **任务完成汇报**: 每个任务完成后，必须显示当前上下文使用情况
  - 格式：`已使用Token: X / 200,000 (XX.X%)`
  - 示例：`已使用Token: 53,264 / 200,000 (26.6%)`
- **优化建议**:
  - 定期清理不需要的后台进程
  - 避免重复读取大文件
  - 及时总结和归档已完成的任务信息

---

## 🚨 任务管理规范（强制遵守）

本项目使用**任务看板系统**进行多AI Agent协作开发。

### 📋 核心文件
- `TASKS.md` - 主看板（全局任务列表）
- `tasks/details/{todo,doing,done,blocked}/` - 任务详情文件

### 🔴 强制规则
1. **工作前必须**: `git pull origin main && cat TASKS.md`
2. **认领后立即提交**: 避免多人冲突
3. **一次一个任务**: 除非有明确许可
4. **禁止修改他人任务**: 只能操作@Kiro的任务
5. **完成必须更新**: 同时更新TASKS.md和详情文件

### ⚡ 快速流程
```bash
# 1. 认领任务
git pull origin main
编辑TASKS.md: @无人认领 → @Kiro
git add TASKS.md && git commit -m "task: 认领 #001" && git push

# 2. 开始任务
移动到DOING区域，移动详情文件
git commit -m "task: 开始 #001"

# 3. 完成任务
移动到DONE，勾选checkbox，填写工时
git commit -m "task: 完成 #001 任务描述"
git push origin main
```

### 📝 Commit格式
`task: <操作> #<编号> <描述>`

### 📚 完整规范
详见: `.claude/claude.md` 的"任务管理规范"章节
