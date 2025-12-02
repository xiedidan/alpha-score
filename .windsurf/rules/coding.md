# Windsurf AI 编码规则

## 项目概述
Binance Alpha 自动化交易工具 - Web管理界面 + 自动化脚本

## 技术栈
- 后端：Python 3.11+ / FastAPI / Playwright / SQLite
- 前端：Vue 3 / TypeScript / Vite / Element Plus
- OSD：PyQt6
- **代理/部署**：
  - 开发环境：Vite Proxy（已配置在vite.config.ts）
  - 生产环境：Caddy（自动HTTPS，配置简单）

## 部署架构决策

### 开发环境
```
[浏览器] → [Vite Dev Server :5173]
            ↓ /api/* 请求
            [Vite Proxy]
            ↓
            [FastAPI :8000]
```
**配置位置**: `frontend/vite.config.ts` → `server.proxy`

### 生产环境
```
[浏览器] → [Caddy :80/:443]
            ↓ /api/* 请求      ↓ 静态文件
            [FastAPI :8000]    [Vue Dist]
```
**配置位置**: `Caddyfile`（项目根目录）

### 架构选型原因
- ✅ **开发**: Vite Proxy - 零配置，开箱即用
- ✅ **生产**: Caddy - 自动HTTPS，配置简单，不影响系统其他服务
- ❌ **不用Nginx** - 避免影响系统现有网站
- ❌ **不用Traefik** - 当前阶段不需要容器编排

## 项目约束
- 隐蔽性：所有自动化操作模拟人类
- 安全性：严格风控,保护资金
- 稳定性：完善异常处理

## 编码标准
- Python：Black + Pylint
- TypeScript：ESLint + Prettier
- 提交：Conventional Commits

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

本项目使用任务看板系统，所有AI Agent必须遵守统一规范。

### 核心规则
1. **工作前同步**: `git pull origin main`
2. **查看任务**: `cat TASKS.md`
3. **认领立即提交**: 编辑TASKS.md后立即push
4. **一次一个任务**: 专注完成当前任务
5. **禁止跨界**: 只操作@Windsurf的任务

### 任务流程
```bash
# 认领
git pull && 编辑TASKS.md(@无人认领→@Windsurf)
git add TASKS.md && git commit -m "task: 认领 #001" && git push

# 开始
移动任务到DOING + 移动详情文件
git commit -m "task: 开始 #001" && git push

# 完成
移动到DONE + 勾选checkbox + 填写工时
git commit -m "task: 完成 #001 描述" && git push
```

### Commit格式
- 认领: `task: 认领 #001 任务名`
- 开始: `task: 开始 #001 任务名`
- 完成: `task: 完成 #001 任务名`
- 阻塞: `task: 阻塞 #001 原因`

### 详细规范
查看: `.claude/claude.md` 和 `tasks/README.md`
