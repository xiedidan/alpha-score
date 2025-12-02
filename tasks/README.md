# 任务管理系统使用指南

> Alpha-Score 项目多AI Agent协作任务管理系统

---

## 📖 目录

1. [系统概述](#系统概述)
2. [文件结构](#文件结构)
3. [快速开始](#快速开始)
4. [详细操作流程](#详细操作流程)
5. [任务状态说明](#任务状态说明)
6. [协作规范](#协作规范)
7. [常见问题](#常见问题)
8. [最佳实践](#最佳实践)

---

## 系统概述

### 设计目标

本任务管理系统专为**多AI Agent并行协作开发**设计，解决以下问题：

- ✅ **避免任务冲突**：明确任务归属，避免重复工作
- ✅ **状态可见**：实时了解项目进度和每个Agent的工作状态
- ✅ **降低冲突**：通过文件分离和即时提交减少Git冲突
- ✅ **灵活协作**：支持快速任务认领和状态更新

### 核心特点

1. **单文件看板** + **文件夹详情** 混合模式
2. 基于Git的同步机制
3. Markdown格式，易读易编辑
4. 支持任务依赖关系管理

---

## 文件结构

```
alpha-score/
├── TASKS.md                    # 主看板（核心文件）
│
├── tasks/
│   ├── README.md               # 使用指南（本文件）
│   ├── TASK_TEMPLATE.md        # 任务模板
│   │
│   └── details/                # 任务详情目录
│       ├── todo/               # 待办任务
│       │   ├── 001-init-backend.md
│       │   └── 002-init-frontend.md
│       │
│       ├── doing/              # 进行中任务
│       │   └── 005-create-structure.md
│       │
│       ├── done/               # 已完成任务
│       │   └── 000-system-design.md
│       │
│       └── blocked/            # 阻塞任务
│           └── 006-deploy-production.md
│
└── .claude/
    └── claude.md               # AI Agent规则（含任务管理规范）
```

### 文件说明

| 文件 | 作用 | 更新频率 |
|------|------|---------|
| **TASKS.md** | 全局任务列表，快速查看所有任务状态 | 每次任务变更 |
| **tasks/details/** | 详细任务描述，包含完整信息 | 任务创建和完成时 |
| **TASK_TEMPLATE.md** | 创建新任务的模板 | 很少修改 |

---

## 快速开始

### 第一次使用

```bash
# 1. 确保在项目根目录
cd /path/to/alpha-score

# 2. 查看任务看板
cat TASKS.md

# 3. 查看待办任务列表
ls tasks/details/todo/

# 4. 查看某个任务详情
cat tasks/details/todo/001-init-backend.md
```

### 认领并开始第一个任务

```bash
# Step 1: 同步最新代码
git pull origin main

# Step 2: 认领任务
# 编辑TASKS.md，将某个任务的 @无人认领 改为 @你的名字
vim TASKS.md  # 或使用其他编辑器

# Step 3: 立即提交
git add TASKS.md
git commit -m "task: 认领 #001"
git push origin main

# Step 4: 开始工作
# 按照任务详情文件的指引开始开发
```

---

## 详细操作流程

### 1. 查看可用任务

#### 方法1：查看主看板
```bash
cat TASKS.md
```

查找标记为 `@无人认领` 的任务。

#### 方法2：列出待办任务文件
```bash
ls -l tasks/details/todo/
```

#### 方法3：搜索特定类型任务
```bash
# 搜索高优先级任务
cat TASKS.md | grep "高🔴"

# 搜索后端相关任务
cat TASKS.md | grep "backend"

# 搜索前端相关任务
cat TASKS.md | grep "frontend"
```

---

### 2. 认领任务

#### 完整流程

```bash
# Step 1: 同步最新代码（必须！）
git pull origin main

# Step 2: 阅读任务详情
cat tasks/details/todo/001-init-backend.md

# Step 3: 检查依赖关系
# 在任务详情中查看"依赖任务"部分
# 确保所有依赖任务已完成

# Step 4: 编辑TASKS.md认领任务
# 将以下内容修改：
# - [ ] #001 xxx @无人认领  →  - [ ] #001 xxx @你的名字
#
# 同时更新"Agent工作分配"表格：
# | Claude | 无 | 💤 空闲 |  →  | Claude | #001 xxx | 🚀 认领 |

# Step 5: 立即提交（避免冲突）
git add TASKS.md
git commit -m "task: 认领 #001"
git push origin main
```

#### 认领失败处理

如果push失败（有人同时修改了TASKS.md）：

```bash
# 拉取最新代码
git pull origin main

# 检查是否有冲突
git status

# 如果有冲突，手动解决冲突
# 打开TASKS.md，保留正确的内容

# 重新提交
git add TASKS.md
git commit -m "task: 认领 #001"
git push origin main
```

---

### 3. 开始任务

```bash
# Step 1: 在TASKS.md中移动任务
# 将任务从 "待办 (TODO)" 区域移动到 "进行中 (DOING)" 区域

# Step 2: 添加开始时间
# 在任务行添加: `开始:2025-11-27 10:00`

# Step 3: 移动详情文件
mv tasks/details/todo/001-init-backend.md tasks/details/doing/

# Step 4: 更新详情文件中的状态
# 编辑 tasks/details/doing/001-init-backend.md
# 将 **状态** 从 TODO 改为 DOING
# 填写 **开始时间**

# Step 5: 更新Agent工作分配表
# | Claude | #001 xxx | 🚀 认领 |  →  | Claude | #001 xxx | 🔥 进行中 |

# Step 6: 提交变更
git add TASKS.md tasks/
git commit -m "task: 开始 #001 初始化后端FastAPI项目"
git push origin main

# Step 7: 开始实际开发工作
```

---

### 4. 开发过程中

#### 记录开发日志

在任务详情文件（`tasks/details/doing/001-*.md`）的"开发日志"部分记录：

```markdown
## 📝 开发日志

### 2025-11-27 10:30 - @Claude
- 创建了虚拟环境
- 安装了所有依赖
- 遇到playwright安装问题，通过 `playwright install` 解决

### 2025-11-27 11:00 - @Claude
- 完成main.py基础代码
- 成功启动服务
- API文档可以正常访问
```

#### 更新进度（可选）

如果任务较长，可以定期更新TASKS.md：

```bash
git add TASKS.md
git commit -m "task: 更新 #001 已完成依赖安装"
git push origin main
```

---

### 5. 完成任务

#### 完整流程

```bash
# Step 1: 确保所有验收标准已满足
# 检查任务详情文件中的"验收标准"部分
# 逐一验证每个条目

# Step 2: 更新TASKS.md
# - 将 [ ] 改为 [x]
# - 将任务从 DOING 移动到 DONE 区域
# - 添加完成时间: `完成:2025-11-27`
# - 添加实际工时: `⏱️ 实际:2h`

# Step 3: 移动详情文件
mv tasks/details/doing/001-init-backend.md tasks/details/done/

# Step 4: 更新详情文件
# 编辑 tasks/details/done/001-init-backend.md
# - 将 **状态** 改为 DONE
# - 填写 **完成时间**
# - 填写 **实际工时**
# - 勾选所有 **验收标准**
# - 勾选 **完成检查清单**

# Step 5: 更新Agent工作分配表
# 将自己的状态改为 💤 空闲

# Step 6: 提交所有变更（包括开发的代码）
git add TASKS.md tasks/ backend/ frontend/ <其他修改的文件>
git commit -m "task: 完成 #001 初始化后端FastAPI项目

- 创建虚拟环境和依赖文件
- 实现基础FastAPI应用
- 添加健康检查接口
- 所有验收标准已满足"

git push origin main
```

#### 通知依赖任务

如果有任务依赖你刚完成的任务，可以：

```bash
# 在任务详情文件末尾添加通知
echo "任务 #001 已完成，以下任务可以开始：#003, #004, #005, #006" >> tasks/details/done/001-init-backend.md

# 或在项目沟通渠道中通知
```

---

### 6. 任务阻塞

当遇到无法继续的情况时：

```bash
# Step 1: 在TASKS.md中移动任务到BLOCKED区域
# Step 2: 添加阻塞原因
# - [ ] #001 xxx `@Claude` `阻塞原因:等待xxx`

# Step 3: 移动详情文件
mv tasks/details/doing/001-*.md tasks/details/blocked/

# Step 4: 在详情文件中详细说明阻塞原因

# Step 5: 提交并通知
git add TASKS.md tasks/
git commit -m "task: 阻塞 #001 等待数据库模型设计完成"
git push origin main

# Step 6: 通知Human或相关Agent
```

---

## 任务状态说明

### 状态流转图

```
     认领         开始         完成
TODO ───→ TODO ───→ DOING ───→ DONE
              ↓
           BLOCKED（如果遇到阻塞）
              ↓
           DOING（阻塞解除后）
```

### 状态定义

| 状态 | 符号 | 说明 | 负责人 |
|------|------|------|--------|
| **TODO** | `- [ ]` | 待办，未认领 | `@无人认领` |
| **TODO** | `- [ ]` | 已认领，未开始 | `@Agent名` |
| **DOING** | `- [ ]` | 进行中 | `@Agent名` |
| **DONE** | `- [x]` | 已完成 | `@Agent名` |
| **BLOCKED** | `- [ ]` | 阻塞/暂停 | `@Agent名` |

---

## 协作规范

### 基本原则

1. **先拉后推**: 任何操作前先 `git pull`
2. **立即提交**: 认领任务后立即提交，不要拖延
3. **专注单任务**: 一次只认领一个任务（除非明确许可）
4. **尊重归属**: 不要修改其他Agent已认领的任务
5. **保持同步**: 完成任务后立即更新状态

### Commit Message规范

统一使用以下格式：

```
task: <操作> #<编号> <简短描述>
```

**操作类型**：
- `认领` - 认领任务
- `开始` - 开始任务
- `更新` - 更新任务信息
- `完成` - 完成任务
- `阻塞` - 任务遇到阻塞

**示例**：
```
task: 认领 #001
task: 开始 #001 初始化后端FastAPI项目
task: 更新 #001 添加依赖安装步骤
task: 完成 #001 初始化后端FastAPI项目
task: 阻塞 #001 等待数据库模型设计
```

### 冲突处理

#### 预防冲突

- 认领前先 `git pull`
- 认领后立即提交推送
- 操作不同的任务（自然隔离）

#### 解决冲突

如果遇到Git冲突：

```bash
# 1. 拉取最新代码
git pull origin main

# 2. 查看冲突文件
git status

# 3. 手动编辑冲突文件
# 打开TASKS.md，找到冲突标记：
# <<<<<<< HEAD
# =======
# >>>>>>> main

# 4. 保留正确的内容（通常是保留所有Agent的修改）

# 5. 标记冲突已解决
git add TASKS.md

# 6. 完成合并
git commit -m "task: 解决冲突"

# 7. 推送
git push origin main
```

---

## 常见问题

### Q1: 如何查看自己当前的任务？

```bash
# 查看自己认领的所有任务
cat TASKS.md | grep "@你的名字"

# 查看自己进行中的任务
cat TASKS.md | grep -A 5 "进行中" | grep "@你的名字"
```

### Q2: 任务太大怎么办？

可以将大任务拆分成多个子任务：

1. 在原任务详情中列出子任务
2. 或创建多个独立任务，设置依赖关系

### Q3: 需要创建新任务怎么办？

```bash
# 1. 复制模板
cp tasks/TASK_TEMPLATE.md tasks/details/todo/XXX-task-name.md

# 2. 编辑新任务文件
# 填写所有必要信息

# 3. 在TASKS.md中添加任务条目

# 4. 提交
git add TASKS.md tasks/
git commit -m "task: 创建新任务 #XXX"
git push origin main
```

### Q4: 发现任务描述不清晰怎么办？

```bash
# 1. 补充任务详情文件
编辑 tasks/details/todo/XXX-*.md

# 2. 在开发日志中记录问题和解决方案

# 3. 提交更新
git commit -m "task: 更新 #XXX 补充任务说明"
```

### Q5: 多个Agent需要协作一个任务怎么办？

在任务详情的"协作说明"部分：
- 明确各Agent的职责
- 定义接口和输出物
- 约定提交顺序

---

## 最佳实践

### 1. 任务认领

✅ **推荐**：
- 认领前阅读完整的任务详情
- 检查依赖关系是否满足
- 评估自己的能力是否匹配
- 认领后立即提交

❌ **避免**：
- 认领后长时间不开始
- 同时认领多个任务
- 认领超出能力范围的任务

### 2. 任务执行

✅ **推荐**：
- 按照验收标准逐项完成
- 及时记录开发日志
- 遇到问题立即在任务中记录
- 代码提交前先更新任务状态

❌ **避免**：
- 跳过验收标准
- 不记录开发过程
- 完成后不更新状态

### 3. 协作沟通

✅ **推荐**：
- 在任务详情中留言沟通
- 完成后通知依赖任务的Agent
- 发现问题及时标记BLOCKED

❌ **避免**：
- 私下沟通不留记录
- 默默解决问题不分享经验
- 遇到阻塞不通知

### 4. Git操作

✅ **推荐**：
```bash
# 操作前
git pull origin main

# 操作中
git add TASKS.md tasks/
git commit -m "task: xxx"

# 操作后
git push origin main
```

❌ **避免**：
- 不拉取直接修改
- 长时间不提交
- 使用 `git push -f`

---

## 附录

### A. 任务优先级说明

| 优先级 | 符号 | 说明 | 处理建议 |
|--------|------|------|---------|
| 高 | 🔴 | 核心功能，阻塞其他任务 | 优先认领和完成 |
| 中 | 🟡 | 重要功能，有一定依赖 | 按顺序处理 |
| 低 | 🟢 | 优化改进，不紧急 | 空闲时处理 |

### B. 任务标签说明

常用标签：
- `backend` - 后端相关
- `frontend` - 前端相关
- `setup` - 环境配置
- `api` - API开发
- `ui` - 界面开发
- `bug` - Bug修复
- `refactor` - 重构
- `test` - 测试
- `docs` - 文档

### C. Agent名称约定

在任务中使用以下标准名称：
- `@Claude` - Claude AI
- `@Cursor` - Cursor AI
- `@Kiro` - Kiro AI
- `@Windsurf` - Windsurf AI
- `@KIMI` - KIMI AI
- `@Human` - 人类开发者

---

## 联系与反馈

- 任务管理问题：查看 `.claude/claude.md` 中的详细规范
- 项目问题：提交Issue或查看 `docs/system_design.md`
- 改进建议：欢迎在任务评论中提出

---

**文档版本**: v1.0
**最后更新**: 2025-11-27
**维护者**: @Claude
