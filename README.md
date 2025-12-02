# Binance Alpha 自动化交易工具

> 自动化获取币安 Alpha 积分和网格交易系统

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
[![Vue Version](https://img.shields.io/badge/vue-3.x-green)](https://vuejs.org/)
[![License](https://img.shields.io/badge/license-MIT-orange)](LICENSE)

## 项目简介

Binance Alpha 自动化交易工具是一个用于自动化获取币安 Alpha 积分的智能交易系统。通过浏览器自动化技术和智能策略引擎，帮助用户最大化积分收益，同时支持网格交易创造额外收益。

### 核心特性

- 🤖 **全自动交易**：自动执行买卖订单，最大化积分获取
- 🛡️ **完善风控**：ATR 检测、仓位控制、止损机制
- 🎭 **隐蔽性设计**：极致模拟人类行为，规避平台风控
- 📊 **Web 管理界面**：实时监控、配置管理、数据分析
- 🖥️ **OSD 实时显示**：透明置顶窗口，不遮挡操作
- 🔄 **网格交易**：自动化网格策略，创造额外收益
- 🧠 **LLM 增强**：市场分析、异常检测、智能决策
- 📱 **多渠道通知**：Discord/Telegram/飞书/PushPlus

### 系统架构

```
┌──────────────────────────────────────────���──────────────┐
│  Web 管理界面    OSD 显示层      通知系统                 │
│  (Vue3+Vite)   (Overlay UI)  (Discord/TG)               │
└─────────────────────────────────────────────────────────┘
                         ↕ HTTP/WebSocket
┌─────────────────────────────────────────────────────────┐
│         后端服务 (Python FastAPI)                         │
│  API 网关 · 认证授权 · 配置管理 · 状态管理                │
└──────────────────��──────────────────────────────────────┘
                         ↕
┌─────────────────────────────────────────────────────────┐
│  策略引擎    风控引擎    数据采集                          │
│  积分优化 · ATR检测 · 盘口监控 · 技术指标                 │
└─────────────────────────────────────────────────────────┘
                         ↕
┌─────────────────────────────────────────────────────────┐
│         浏览器自动化引擎 (Playwright)                      │
│  交易执行 · 行为模拟 · 页面控制 · 会话管理                 │
└─────────────────────────────────────────────────────────┘
```

## 快速开始

### 环境要求

- Python 3.11+
- Node.js 18+
- Chrome/Edge ���览器
- Windows 11 (推荐使用 Hyper-V 虚拟机)

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/yourusername/alpha-score.git
cd alpha-score
```

2. **配置敏感信息**
```bash
cp config/secrets.yaml.example config/secrets.yaml
# 编辑 config/secrets.yaml 填入真实的密钥信息
```

3. **安装后端依赖**
```bash
cd backend
pip install -r requirements.txt
playwright install chromium
```

4. **安装前端依赖**
```bash
cd ../frontend
npm install
```

5. **启动浏览器（调试模式）**

Windows:
```bash
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\ChromeDebug"
```

Linux/Mac:
```bash
google-chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-debug
```

6. **手动登录币安 Alpha 平台**

在启动的浏览器中访问币安 Alpha 平台并完成登录

7. **启动后端服务**
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

8. **启动前端服务**
```bash
cd frontend
npm run dev
```

9. **访问 Web 管理界面**

打开浏览器访问：http://localhost:5173

默认用户名：`admin`（在 secrets.yaml 中配置）

### 配置说明

#### 主配置文件 (`config/settings.yaml`)

```yaml
# 交易配置
trading:
  symbol: "KOGE/USDT"        # 交易对
  buy_offset_bp: 10          # 买单偏移量
  sell_offset_bp: -10        # 卖单偏移量
  position_ratio: 0.5        # 单次下单仓位比例

# 风控配置
risk:
  max_atr: 0.01              # 最大 ATR 限制
  max_daily_volume: 50000    # 每日最大交易量
  stop_loss: 100             # 总止损金额
```

#### 阶梯配置文件 (`config/ladders.yaml`)

配置资金阶梯和交易量阶梯，用于积分计算。可通过 Web 界面的"阶梯设计器"可视化编辑。

## 功能文档

### 1. 积分自动获取

- 自动计算目标积分所需交易量
- 智能订单生成（反向限价单）
- 磨损最小化策略
- 达到��标自动停止

### 2. 风控系统

- **市场风控**：ATR 检测、价格波动监控
- **仓位风控**：持仓比例、单日交易量限制
- **亏损风控**：连续亏损、总亏损控制
- **异常风控**：登录状态、网络连接检测

### 3. 行为模拟

- 随机延迟（1-3 秒）
- 贝塞尔曲线鼠标移动
- 随机浏览行为（滚动、悬停、阅读）
- 操作随机化

### 4. Web 管理界面

- **仪表盘**：实时监控交易状态和积分进度
- **交易监控**：交易列表、K 线图表、盘口深度
- **参数配置**：积分配置、阶梯设计器、风控参数
- **历史数据**：交易历史、积分趋势、磨损分析
- **日志查询**：系统日志、错误日志、交易日志

### 5. OSD 实时显示

透明置顶窗口，实时显示：
- 当前积分/目标积分
- 今日交易额
- 磨损统计
- 盘口信息
- 预测磨损

### 6. 网格交易

- 自动化网格策略
- 支持多种参数配置方式
- 止损止盈机制
- 收益统计分析

## 开发指南

### 项目结构

```
alpha-score/
├── .claude/              # Claude AI 配置
├── .cursor/              # Cursor AI 配置
├── .kiro/                # Kiro AI 配置
├── .windsurf/            # Windsurf AI 配置
├── prompts/              # 其他 AI 提示词
├── backend/              # 后端代码
│   ├── api/              # API 路由
│   ├── modules/          # 核心模块
│   ├── models/           # 数据模型
│   └── utils/            # 工具函数
├── frontend/             # 前端代码
│   ├── src/              # 源代码
│   ├── public/           # 静态资源
│   └── package.json      # 依赖配置
├── config/               # 配置文件
├── data/                 # 数据存储
├── logs/                 # 日志文件
├── docs/                 # 项目文档
└── tests/                # 测试代码
```

### 开发规范

- **Python**：PEP 8 + Black + Type Hints
- **TypeScript**：ESLint + Prettier + Strict Mode
- **Git**：Conventional Commits

### 运行测试

```bash
# 后端单元测试
cd backend
pytest tests/unit/

# 前端单元测试
cd frontend
npm run test:unit

# 集成测试
pytest tests/integration/

# E2E 测试
pytest tests/e2e/
```

## 风险提示

⚠️ **重要声明**

- 本系统可能违反币安服务条款
- 自动化交易存在资金损失风险
- 用户需自行承担所有法律和财务风险
- 仅供个人学习和研究使用
- 不得用于商业用途

⚠️ **使用建议**

1. 小额资金测试，验证策略有效性
2. 严格设置风控参数
3. 定期检查系统运行状态
4. 及时更新行为模拟策略
5. 不要过度依赖自动化系统

## 常见问题

### Q1: 如何避免被平台检测？

- 使用远程调试连接已登录浏览器
- 启用完整的行为模拟功能
- 设置合理的延迟范围
- 避免规律性操作
- 小额起步，逐步放大

### Q2: 磨损如何最小化？

- 使用反向限价单策略
- 选择流动性好的交易对
- 调整偏移量参数
- 监控价差和 ATR
- 避免在剧烈波动时交易

### Q3: 如何设置合理的风控参数？

- 根据账户资金量设置仓位比例
- 根据币种特性设置 ATR 限制
- 根据风险承受能力设置止损
- 定期评估和调整参数
- 参考历史数据优化策略

## 路线图

- [x] 项目架构设计
- [x] 目录结构创建
- [x] AI 提示词配置
- [x] 配置文件设计
- [ ] Web 管理界面开发
- [ ] OSD 显示模块
- [ ] LLM 能力接入
- [ ] MVP 核心功能
- [ ] 完整系统测试
- [ ] 网格交易功能

## 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 联系方式

- 项目主页：https://github.com/yourusername/alpha-score
- 问题反馈：https://github.com/yourusername/alpha-score/issues

## 致谢

感谢所有为本项目做出贡献的开发者！

---

**免责声明**：本软件仅供学习研究使用，使用本软件造成的任何损失由使用者自行承担。
