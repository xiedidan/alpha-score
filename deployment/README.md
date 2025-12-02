# 部署文档总览

## 简介

本目录包含Alpha-Score项目的所有部署配置和文档，支持多种部署方式。

## 目录结构

```
deployment/
├── caddy/              # Caddy反向代理配置
│   ├── Caddyfile      # Caddy配置文件
│   └── README.md      # Caddy部署文档
├── docker/            # Docker容器化部署
│   ├── Dockerfile.backend       # 后端镜像
│   ├── Dockerfile.frontend      # 前端镜像
│   ├── docker-compose.yml       # 服务编排
│   ├── .dockerignore           # Docker忽略文件
│   └── README.md               # Docker部署文档
├── nginx/             # Nginx反向代理配置
│   ├── nginx.conf     # Nginx配置文件
│   └── README.md      # Nginx部署文档
├── systemd/           # Systemd服务配置
│   ├── alpha-score-backend.service   # 后端服务
│   ├── alpha-score-frontend.service  # 前端服务
│   └── README.md                     # Systemd部署文档
└── README.md          # 本文件
```

## 部署方式对比

| 方式 | 适用场景 | 难度 | 推荐度 |
|------|---------|------|--------|
| **Docker Compose** | 快速部署、开发环境、容器化 | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Systemd + Nginx** | 生产环境、Linux服务器 | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Systemd + Caddy** | 自动HTTPS、简化配置 | ⭐⭐ | ⭐⭐⭐⭐ |
| **手动部署** | 开发调试 | ⭐ | ⭐⭐ |

## 快速选择

### 我想快速体验项目
→ 使用 **Docker Compose**
```bash
cd deployment/docker
docker-compose up -d
```

### 我要部署到生产服务器
→ 使用 **Systemd + Nginx** 或 **Docker Compose**

详见下方"推荐部署方案"

### 我只是本地开发
→ 使用 **手动启动**
```bash
# 终端1 - 后端
cd backend
./venv/bin/uvicorn main:app --reload

# 终端2 - 前端
cd frontend
npm run dev
```

## 推荐部署方案

### 方案1: Docker Compose（推荐新手）

**优点**:
- 一键部署，配置简单
- 环境隔离，依赖清晰
- 易于迁移和扩展
- 包含自动重启

**步骤**:
```bash
# 1. 克隆项目
git clone <repository>
cd alpha-score

# 2. 配置环境变量
cp .env.example .env
nano .env

# 3. 启动服务
cd deployment/docker
docker-compose up -d

# 4. 查看日志
docker-compose logs -f
```

**详细文档**: [deployment/docker/README.md](docker/README.md)

### 方案2: Systemd + Nginx（推荐生产）

**优点**:
- 性能最优
- 资源占用低
- 完全掌控
- 便于监控

**步骤**:
```bash
# 1. 部署后端服务
sudo cp deployment/systemd/alpha-score-backend.service /etc/systemd/system/
sudo systemctl enable alpha-score-backend
sudo systemctl start alpha-score-backend

# 2. 构建前端
cd frontend
npm run build

# 3. 部署Nginx
sudo cp deployment/nginx/nginx.conf /etc/nginx/sites-available/alpha-score
sudo ln -s /etc/nginx/sites-available/alpha-score /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# 4. 配置SSL（可选）
sudo certbot --nginx -d your-domain.com
```

**详细文档**:
- [deployment/systemd/README.md](systemd/README.md)
- [deployment/nginx/README.md](nginx/README.md)

### 方案3: Systemd + Caddy（推荐自动HTTPS）

**优点**:
- 自动HTTPS证书
- 配置极简
- 内置健康检查

**步骤**:
```bash
# 1. 部署后端服务
sudo cp deployment/systemd/alpha-score-backend.service /etc/systemd/system/
sudo systemctl enable alpha-score-backend
sudo systemctl start alpha-score-backend

# 2. 构建前端
cd frontend
npm run build

# 3. 部署Caddy
sudo apt install caddy
sudo cp deployment/caddy/Caddyfile /etc/caddy/Caddyfile
# 修改域名
sudo nano /etc/caddy/Caddyfile
sudo systemctl restart caddy
```

**详细文档**: [deployment/caddy/README.md](caddy/README.md)

## 环境要求

### 最低要求
- **CPU**: 1核
- **内存**: 1GB
- **磁盘**: 10GB
- **系统**: Ubuntu 20.04+ / Debian 11+ / CentOS 8+

### 推荐配置
- **CPU**: 2核
- **内存**: 2GB
- **磁盘**: 20GB SSD
- **系统**: Ubuntu 22.04 LTS

### 软件依赖

**方案1 (Docker)**:
- Docker 20.10+
- Docker Compose 2.0+

**方案2 (Systemd + Nginx)**:
- Python 3.11+
- Node.js 20+
- Nginx 1.18+
- SQLite 3+ (或PostgreSQL 13+)

**方案3 (Systemd + Caddy)**:
- Python 3.11+
- Node.js 20+
- Caddy 2.0+

## 部署前检查清单

### 1. 配置文件

- [ ] 创建并配置 `.env` 文件
- [ ] 修改 `config/secrets.yaml`（JWT密钥、API密钥）
- [ ] 检查 `config/settings.yaml`（端口、数据库路径）
- [ ] 如果使用域名，修改反向代理配置中的域名

### 2. 安全检查

- [ ] 更改默认管理员密码
- [ ] 生成强随机JWT密钥
- [ ] 配置防火墙规则
- [ ] 禁用不必要的端口
- [ ] 配置HTTPS证书

### 3. 数据准备

- [ ] 初始化数据库
- [ ] 创建必要目录（logs/, data/）
- [ ] 设置正确的文件权限

## 部署后验证

### 1. 服务状态检查

```bash
# Docker方式
docker-compose ps
docker-compose logs

# Systemd方式
sudo systemctl status alpha-score-backend
sudo systemctl status nginx
```

### 2. 端点测试

```bash
# 健康检查
curl http://localhost:8000/health

# API测试
curl http://localhost:8000/api

# 前端访问
curl http://localhost/
```

### 3. 日志检查

```bash
# 后端日志
tail -f logs/app/app_*.log

# Nginx日志
sudo tail -f /var/log/nginx/alpha-score-access.log

# Docker日志
docker-compose logs -f backend
```

## 常见问题

### Q: 如何更新应用？

**Docker方式**:
```bash
cd deployment/docker
docker-compose pull
docker-compose up -d --build
```

**Systemd方式**:
```bash
# 更新代码
git pull

# 重启后端
sudo systemctl restart alpha-score-backend

# 重新构建前端
cd frontend
npm run build
```

### Q: 如何备份数据？

```bash
# 备份数据库
cp data/alpha.db data/alpha.db.backup-$(date +%Y%m%d)

# 备份配置
tar czf config-backup-$(date +%Y%m%d).tar.gz config/

# 备份日志
tar czf logs-backup-$(date +%Y%m%d).tar.gz logs/
```

### Q: 如何查看错误日志？

```bash
# 应用日志
tail -100 logs/error/error_$(date +%Y-%m-%d).log

# Systemd日志
sudo journalctl -u alpha-score-backend -n 100

# Docker日志
docker-compose logs --tail=100 backend
```

### Q: 如何重置管理员密码？

```bash
# 进入后端目录
cd backend

# 运行密码重置脚本（需要创建）
./venv/bin/python -c "
from models.user import User
from database import SessionLocal

db = SessionLocal()
user = db.query(User).filter(User.username == 'admin').first()
user.set_password('new_password')
db.commit()
print('Password reset successfully')
"
```

## 监控和维护

### 日志轮转

日志文件会自动轮转压缩，配置在 `backend/utils/logger.py`

### 磁盘空间监控

```bash
# 检查磁盘使用
df -h

# 清理旧日志（超过30天）
find logs/ -name "*.log" -mtime +30 -delete
find logs/ -name "*.zip" -mtime +60 -delete
```

### 性能监控

```bash
# 系统资源
htop

# 进程监控
ps aux | grep uvicorn
ps aux | grep nginx

# 网络连接
netstat -tlnp | grep :8000
```

## 安全建议

1. **使用HTTPS**: 生产环境必须配置SSL/TLS
2. **防火墙**: 只开放必要端口（80, 443）
3. **定期更新**: 及时更新系统和依赖包
4. **备份策略**: 每日备份数据库和配置
5. **监控告警**: 配置服务异常告警
6. **访问控制**: 限制管理接口访问IP
7. **日志审计**: 定期审查访问日志

## 扩展和优化

### 水平扩展

使用负载均衡器（Nginx/HAProxy）+ 多个后端实例

### 数据库升级

从SQLite迁移到PostgreSQL/MySQL以提升性能

### CDN加速

静态资源使用CDN（Cloudflare, AWS CloudFront等）

### 缓存优化

- 使用Redis缓存热数据
- Nginx配置静态资源缓存
- API响应缓存

## 故障恢复

### 服务无响应

```bash
# 重启服务
sudo systemctl restart alpha-score-backend
sudo systemctl restart nginx

# 或Docker
docker-compose restart
```

### 数据库损坏

```bash
# 从备份恢复
cp data/alpha.db.backup-20251201 data/alpha.db
sudo systemctl restart alpha-score-backend
```

### 磁盘空间不足

```bash
# 清理日志
find logs/ -name "*.log" -mtime +7 -delete

# 清理Docker
docker system prune -a
```

## 技术支持

- **文档**: 各子目录的README.md
- **问题追踪**: GitHub Issues
- **项目主页**: [README.md](../README.md)

## 更新日志

- **2025-12-02**: 创建部署文档，添加Docker、Systemd、Nginx、Caddy配置
