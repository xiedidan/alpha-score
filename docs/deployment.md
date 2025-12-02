# Alpha-Score 部署指南

## 架构概览

### 开发环境
```
[浏览器] → [Vite Dev Server :5173 + Proxy] → [FastAPI :8000]
```

### 生产环境
```
[浏览器] → [Caddy :80/:443] → [FastAPI :8000]
                           ↓ 静态文件
                       [Vue Dist]
```

---

## 开发环境部署

### 1. 后端启动
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python scripts/init_db.py  # 初始化数据库
python main.py  # 启动FastAPI (http://localhost:8000)
```

### 2. 前端启动
```bash
cd frontend
npm install
npm run dev  # 启动Vite (http://localhost:5173)
```

### 3. 访问应用
- 前端: http://localhost:5173
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs
- 默认账户: admin / admin123

### 配置文件
- 前端代理: `frontend/vite.config.ts` → `server.proxy`
- 后端CORS: `backend/main.py` → `CORSMiddleware`
- 环境变量: `frontend/.env`

---

## 生产环境部署

### 方案：Caddy 反向代理

#### 为什么选择Caddy？
- ✅ 自动HTTPS证书（Let's Encrypt）
- ✅ 配置简单，人类可读
- ✅ 高性能（Go语言）
- ✅ 不影响系统其他网站
- ✅ 自动压缩和缓存

#### 1. 安装Caddy
```bash
# Ubuntu/Debian
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update
sudo apt install caddy

# macOS
brew install caddy

# 手动安装（所有平台）
# 下载: https://github.com/caddyserver/caddy/releases
```

#### 2. 构建前端
```bash
cd frontend
npm run build
# 产物在 frontend/dist/
```

#### 3. 配置Caddy
编辑项目根目录的 `Caddyfile`：

```caddyfile
your-domain.com {
    # 自动HTTPS
    tls your-email@example.com

    # API代理
    reverse_proxy /api/* localhost:8000
    reverse_proxy /ws/* localhost:8000

    # 静态文件
    root * /path/to/alpha-score/frontend/dist
    try_files {path} /index.html
    file_server

    encode gzip
}
```

#### 4. 启动后端服务（systemd）
创建 `/etc/systemd/system/alpha-score-backend.service`:

```ini
[Unit]
Description=Alpha-Score Backend API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/alpha-score/backend
Environment="PATH=/path/to/alpha-score/backend/venv/bin"
ExecStart=/path/to/alpha-score/backend/venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000 --workers 4
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：
```bash
sudo systemctl daemon-reload
sudo systemctl enable alpha-score-backend
sudo systemctl start alpha-score-backend
sudo systemctl status alpha-score-backend
```

#### 5. 启动Caddy
```bash
# 测试配置
caddy validate --config Caddyfile

# 启动Caddy（前台）
caddy run --config Caddyfile

# 或使用systemd（推荐）
sudo systemctl enable caddy
sudo systemctl start caddy
sudo systemctl status caddy
```

#### 6. 防火墙设置
```bash
# 允许HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

---

## Docker部署（可选）

### Docker Compose
创建 `docker-compose.yml`:

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "127.0.0.1:8000:8000"
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    environment:
      - DATABASE_URL=sqlite:///./data/alpha-score.db
    restart: unless-stopped

  caddy:
    image: caddy:2-alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile
      - ./frontend/dist:/var/www/html
      - caddy_data:/data
      - caddy_config:/config
    restart: unless-stopped
    depends_on:
      - backend

volumes:
  caddy_data:
  caddy_config:
```

启动：
```bash
docker-compose up -d
```

---

## 性能优化

### 后端优化
```bash
# 使用多个worker
uvicorn main:app --workers 4

# 或使用gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### 前端优化
- ✅ Vite自动代码分割
- ✅ Gzip压缩（Caddy自动）
- ✅ 静态资源缓存
- ✅ CDN加速（可选）

### Caddy优化
```caddyfile
{
    # 全局选项
    servers {
        protocol {
            experimental_http3  # HTTP/3支持
        }
    }
}
```

---

## 监控与维护

### 日志位置
- Caddy日志: `/var/log/caddy/alpha-score.log`
- 后端日志: `logs/backend_*.log`
- 系统日志: `journalctl -u alpha-score-backend -f`

### 健康检查
```bash
# 后端健康检查
curl http://localhost:8000/health

# Caddy状态（如果启用admin）
curl localhost:2019/config/
```

### 自动更新HTTPS证书
Caddy会自动续期Let's Encrypt证书，无需手动操作。

---

## 故障排查

### 前端无法访问
1. 检查Caddy是否运行: `systemctl status caddy`
2. 检查防火墙: `sudo ufw status`
3. 检查日志: `journalctl -u caddy -n 50`

### 后端API错误
1. 检查服务状态: `systemctl status alpha-score-backend`
2. 检查日志: `journalctl -u alpha-score-backend -f`
3. 手动测试: `curl http://localhost:8000/health`

### HTTPS证书问题
1. 确保域名DNS已正确解析
2. 确保80/443端口开放
3. 检查Caddy日志: `journalctl -u caddy -f`

---

## 回滚方案

### 前端回滚
```bash
cd frontend
git checkout <commit-hash>
npm run build
sudo systemctl reload caddy
```

### 后端回滚
```bash
cd backend
git checkout <commit-hash>
sudo systemctl restart alpha-score-backend
```

---

## 架构决策记录

### 为什么不用Nginx？
- 系统已有其他网站使用Nginx
- 避免配置冲突和相互影响
- Caddy配置更简单

### 为什么不用Traefik？
- 当前阶段不需要容器编排
- Caddy对单机部署更友好
- 配置文件更直观

### 为什么开发用Vite Proxy？
- 零配置，开箱即用
- 热重载支持
- 与Vite完美集成

---

## 安全建议

1. ✅ 使用HTTPS（Caddy自动）
2. ✅ 启用防火墙（ufw）
3. ✅ 定期更新依赖
4. ✅ 修改默认密码
5. ✅ 限制API访问速率
6. ✅ 备份数据库

---

## 相关文档

- Caddy官方文档: https://caddyserver.com/docs/
- FastAPI部署: https://fastapi.tiangolo.com/deployment/
- Vite生产构建: https://vitejs.dev/guide/build.html
