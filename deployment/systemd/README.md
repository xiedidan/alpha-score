# Systemd服务部署指南

## 简介

本目录包含Alpha-Score项目的systemd服务配置，用于在Linux系统上以服务方式运行应用。

## 文件说明

- `alpha-score-backend.service` - 后端API服务
- `alpha-score-frontend.service` - 前端开发服务器（仅用于开发）

## 安装服务

### 1. 准备工作

```bash
# 创建日志目录
mkdir -p /home/xd/project/alpha-score/logs/systemd

# 确保虚拟环境已创建
cd /home/xd/project/alpha-score/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. 安装后端服务

```bash
# 复制服务文件到系统目录
sudo cp deployment/systemd/alpha-score-backend.service /etc/systemd/system/

# 重载systemd配置
sudo systemctl daemon-reload

# 启用服务（开机自启）
sudo systemctl enable alpha-score-backend

# 启动服务
sudo systemctl start alpha-score-backend

# 查看状态
sudo systemctl status alpha-score-backend
```

### 3. 安装前端服务（可选，开发环境）

```bash
# 前端生产环境建议使用Nginx托管静态文件，无需此服务

# 如果需要开发服务器
sudo cp deployment/systemd/alpha-score-frontend.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable alpha-score-frontend
sudo systemctl start alpha-score-frontend
```

## 服务管理

### 启动服务

```bash
# 启动后端
sudo systemctl start alpha-score-backend

# 启动前端
sudo systemctl start alpha-score-frontend
```

### 停止服务

```bash
# 停止后端
sudo systemctl stop alpha-score-backend

# 停止前端
sudo systemctl stop alpha-score-frontend
```

### 重启服务

```bash
# 重启后端
sudo systemctl restart alpha-score-backend

# 重启前端
sudo systemctl restart alpha-score-frontend
```

### 查看状态

```bash
# 查看后端状态
sudo systemctl status alpha-score-backend

# 查看前端状态
sudo systemctl status alpha-score-frontend

# 查看所有Alpha-Score服务
sudo systemctl list-units | grep alpha-score
```

### 开机自启

```bash
# 启用开机自启
sudo systemctl enable alpha-score-backend

# 禁用开机自启
sudo systemctl disable alpha-score-backend

# 查看是否启用
sudo systemctl is-enabled alpha-score-backend
```

## 查看日志

### systemd日志

```bash
# 查看后端日志
sudo journalctl -u alpha-score-backend

# 实时跟踪日志
sudo journalctl -u alpha-score-backend -f

# 查看最近100行
sudo journalctl -u alpha-score-backend -n 100

# 查看今天的日志
sudo journalctl -u alpha-score-backend --since today

# 查看特定时间范围
sudo journalctl -u alpha-score-backend --since "2025-12-01" --until "2025-12-02"
```

### 应用日志文件

```bash
# 查看标准输出日志
tail -f /home/xd/project/alpha-score/logs/systemd/backend-stdout.log

# 查看错误日志
tail -f /home/xd/project/alpha-score/logs/systemd/backend-stderr.log

# 查看应用日志
tail -f /home/xd/project/alpha-score/logs/app/app_*.log
```

## 配置说明

### 服务配置项

#### [Unit]
- `Description`: 服务描述
- `After`: 依赖的服务，确保在网络启动后运行

#### [Service]
- `Type=simple`: 简单服务类型
- `User/Group`: 运行服务的用户和组
- `WorkingDirectory`: 工作目录
- `Environment`: 环境变量
- `ExecStart`: 启动命令
- `Restart=always`: 总是自动重启
- `RestartSec=10`: 重启间隔10秒

#### 资源限制
- `LimitNOFILE`: 文件描述符限制
- `MemoryLimit`: 内存限制
- `CPUQuota`: CPU配额

#### 安全加固
- `NoNewPrivileges`: 禁止提升权限
- `PrivateTmp`: 私有临时目录

### 修改配置

1. 编辑服务文件

```bash
# 直接编辑
sudo nano /etc/systemd/system/alpha-score-backend.service

# 或使用systemctl edit
sudo systemctl edit alpha-score-backend --full
```

2. 重载配置

```bash
sudo systemctl daemon-reload
sudo systemctl restart alpha-score-backend
```

## 生产环境建议

### 1. 使用Gunicorn（多进程）

修改 `ExecStart`：

```ini
ExecStart=/home/xd/project/alpha-score/backend/venv/bin/gunicorn \
    main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --access-logfile /home/xd/project/alpha-score/logs/systemd/gunicorn-access.log \
    --error-logfile /home/xd/project/alpha-score/logs/systemd/gunicorn-error.log \
    --log-level info
```

### 2. 前端使用Nginx

前端生产环境不应使用开发服务器，而应：

1. 构建前端
```bash
cd /home/xd/project/alpha-score/frontend
npm run build
```

2. 使用Nginx托管（见 `deployment/nginx/`）

### 3. 配置反向代理

- 使用Nginx或Caddy作为反向代理
- 不要直接暴露后端端口到公网
- 配置SSL/TLS证书

### 4. 监控和告警

```bash
# 配置邮件告警（失败时发送邮件）
# 在service文件中添加
[Service]
OnFailure=status-email@%n.service
```

## 故障排查

### 服务无法启动

```bash
# 查看详细错误
sudo journalctl -u alpha-score-backend -n 50 --no-pager

# 检查服务配置
sudo systemctl show alpha-score-backend

# 验证配置文件语法
sudo systemd-analyze verify /etc/systemd/system/alpha-score-backend.service
```

### 权限问题

```bash
# 检查文件权限
ls -la /home/xd/project/alpha-score/backend

# 确保用户有执行权限
sudo chown -R xd:xd /home/xd/project/alpha-score

# 检查日志目录权限
sudo chmod -R 755 /home/xd/project/alpha-score/logs
```

### 端口占用

```bash
# 检查端口占用
sudo lsof -i:8000

# 杀死占用进程
sudo kill -9 <PID>

# 或修改服务文件中的端口
```

### 服务频繁重启

```bash
# 查看重启历史
sudo systemctl status alpha-score-backend

# 调整重启策略
[Service]
Restart=on-failure
RestartSec=30
StartLimitBurst=5
StartLimitIntervalSec=300
```

## 性能优化

### Worker数量

后端worker数量建议：
```
workers = (CPU核心数 × 2) + 1
```

### 资源限制

根据实际需求调整：

```ini
[Service]
# 内存限制（根据实际需求）
MemoryLimit=2G

# CPU配额（200% = 2个核心）
CPUQuota=200%

# 文件描述符
LimitNOFILE=65535
```

## 卸载服务

```bash
# 停止服务
sudo systemctl stop alpha-score-backend
sudo systemctl stop alpha-score-frontend

# 禁用服务
sudo systemctl disable alpha-score-backend
sudo systemctl disable alpha-score-frontend

# 删除服务文件
sudo rm /etc/systemd/system/alpha-score-backend.service
sudo rm /etc/systemd/system/alpha-score-frontend.service

# 重载配置
sudo systemctl daemon-reload
```

## 相关链接

- [systemd官方文档](https://www.freedesktop.org/software/systemd/man/)
- [systemd服务管理](https://www.freedesktop.org/software/systemd/man/systemd.service.html)
- [journalctl日志管理](https://www.freedesktop.org/software/systemd/man/journalctl.html)
