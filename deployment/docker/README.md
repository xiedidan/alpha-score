# Docker部署指南

## 简介

本目录包含Alpha-Score项目的Docker容器化配置，支持快速部署和环境隔离。

## 文件说明

- `Dockerfile.backend` - 后端服务镜像
- `Dockerfile.frontend` - 前端服务镜像
- `docker-compose.yml` - 完整服务编排
- `.dockerignore` - Docker构建忽略文件

## 快速开始

### 前置要求

- Docker 20.10+
- Docker Compose 2.0+

### 一键启动

```bash
# 进入部署目录
cd deployment/docker

# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### 访问应用

- 前端: http://localhost
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs

## 详细使用

### 1. 构建镜像

```bash
# 仅构建后端
docker-compose build backend

# 仅构建前端
docker-compose build frontend

# 构建所有服务
docker-compose build
```

### 2. 启动服务

```bash
# 启动所有服务（后台）
docker-compose up -d

# 启动指定服务
docker-compose up -d backend

# 启动并查看日志
docker-compose up
```

### 3. 使用Caddy反向代理

```bash
# 使用caddy profile启动
docker-compose --profile caddy up -d

# 此时前端服务会被禁用，改用Caddy提供静态文件和反向代理
```

### 4. 服务管理

```bash
# 停止服务
docker-compose stop

# 停止并删除容器
docker-compose down

# 停止并删除容器+数据卷
docker-compose down -v

# 重启服务
docker-compose restart

# 重启指定服务
docker-compose restart backend
```

### 5. 查看日志

```bash
# 查看所有日志
docker-compose logs

# 实时跟踪日志
docker-compose logs -f

# 查看指定服务日志
docker-compose logs -f backend

# 查看最近100行日志
docker-compose logs --tail=100
```

### 6. 进入容器

```bash
# 进入后端容器
docker-compose exec backend sh

# 进入前端容器
docker-compose exec frontend sh

# 执行命令
docker-compose exec backend python -c "print('Hello')"
```

## 环境配置

### 环境变量

创建 `.env` 文件在项目根目录：

```bash
# 后端配置
BACKEND_PORT=8000
PYTHONUNBUFFERED=1

# 前端配置
FRONTEND_PORT=80

# 数据库（如果使用）
DATABASE_URL=sqlite:///./data/alpha.db

# JWT密钥（生产环境务必修改）
JWT_SECRET_KEY=your-super-secret-key-here

# 其他配置...
```

### 配置文件挂载

配置文件通过volume挂载：
- `config/` → `/app/config` (只读)
- `logs/` → `/app/logs` (读写)
- `data/` → `/app/data` (读写)

## 生产部署

### 1. 修改配置

```bash
# 1. 创建生产环境配置
cp .env.example .env
nano .env

# 2. 修改敏感配置
nano config/secrets.yaml
```

### 2. 使用外部数据库

修改 `docker-compose.yml` 添加数据库服务：

```yaml
services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: alpha_score
      POSTGRES_USER: alpha
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### 3. HTTPS配置

使用Caddy自动HTTPS：

```bash
# 1. 修改Caddyfile，将localhost改为实际域名
nano ../caddy/Caddyfile

# 2. 启动Caddy服务
docker-compose --profile caddy up -d
```

### 4. 资源限制

在 `docker-compose.yml` 中添加资源限制：

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
        reservations:
          memory: 512M
```

## 故障排查

### 容器无法启动

```bash
# 查看详细错误
docker-compose logs backend

# 检查容器状态
docker-compose ps

# 检查资源使用
docker stats
```

### 网络连接问题

```bash
# 检查网络
docker network ls
docker network inspect alpha-score_alpha-network

# 重建网络
docker-compose down
docker-compose up -d
```

### 数据持久化问题

```bash
# 查看数据卷
docker volume ls

# 检查数据卷内容
docker run --rm -v alpha-score_data:/data alpine ls -la /data
```

### 重建所有容器

```bash
# 完全清理
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

## 性能优化

### 1. 多阶段构建

Dockerfile已使用多阶段构建，最小化镜像体积。

### 2. 层缓存优化

- 依赖安装层单独缓存
- 代码复制在最后，避免频繁重建

### 3. 资源限制

```yaml
deploy:
  resources:
    limits:
      cpus: '2'
      memory: 2G
```

## 监控和日志

### 日志配置

已配置JSON格式日志，限制文件大小和数量：
- 单文件最大: 10MB
- 保留文件数: 3个

### 健康检查

所有服务都配置了健康检查：
- 检查间隔: 30秒
- 超时时间: 5秒
- 重试次数: 3次

## 备份和恢复

### 备份数据

```bash
# 备份数据卷
docker run --rm -v alpha-score_data:/data -v $(pwd):/backup alpine \
    tar czf /backup/data-backup-$(date +%Y%m%d).tar.gz -C /data .

# 备份配置
tar czf config-backup-$(date +%Y%m%d).tar.gz ../../config
```

### 恢复数据

```bash
# 恢复数据卷
docker run --rm -v alpha-score_data:/data -v $(pwd):/backup alpine \
    tar xzf /backup/data-backup-20251201.tar.gz -C /data
```

## 相关链接

- [Docker官方文档](https://docs.docker.com/)
- [Docker Compose文档](https://docs.docker.com/compose/)
- [最佳实践](https://docs.docker.com/develop/dev-best-practices/)
