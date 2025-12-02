# Caddy 部署配置

## 简介

Caddy是一个现代化的Web服务器，自动处理HTTPS证书，配置简单。本目录包含Alpha-Score项目的Caddy反向代理配置。

## 文件说明

- `Caddyfile` - Caddy主配置文件

## 功能特性

1. **反向代理**
   - API请求代理到后端 (localhost:8000)
   - WebSocket支持
   - 健康检查

2. **静态文件服务**
   - 前端资源托管
   - SPA路由支持 (try_files)

3. **安全增强**
   - HSTS (Strict-Transport-Security)
   - X-Frame-Options
   - X-Content-Type-Options
   - Content-Security-Policy

4. **性能优化**
   - Gzip/Zstd压缩

## 使用方法

### 开发环境

```bash
# 安装Caddy
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update
sudo apt install caddy

# 启动Caddy
cd /home/xd/project/alpha-score/deployment/caddy
caddy run
```

### 生产环境

```bash
# 复制配置到系统目录
sudo cp Caddyfile /etc/caddy/Caddyfile

# 修改配置中的域名和路径
sudo nano /etc/caddy/Caddyfile

# 启动Caddy服务
sudo systemctl enable caddy
sudo systemctl start caddy

# 查看状态
sudo systemctl status caddy
```

## 配置说明

### localhost部分

开发环境配置，用于本地调试：
- 监听localhost
- API代理到8000端口
- 静态文件从构建目录提供

### 生产域名配置

需要修改的部分：
1. 将`localhost`改为实际域名 (如 `alpha-score.example.com`)
2. 修改静态文件路径为实际部署路径
3. 确保后端API端口正确

示例：
```caddyfile
alpha-score.example.com {
    # API proxy
    reverse_proxy /api/* localhost:8000 {
        health_uri /health
        health_interval 10s
    }

    # Static files
    root * /var/www/alpha-score/dist
    try_files {path} /index.html
    file_server
}
```

## 故障排查

### 查看日志
```bash
# 系统日志
sudo journalctl -u caddy -f

# Caddy日志
tail -f /var/log/caddy/access.log
```

### 测试配置
```bash
caddy validate --config /etc/caddy/Caddyfile
```

### 重载配置
```bash
sudo systemctl reload caddy
```

## 注意事项

1. **HTTPS证书**: Caddy会自动申请Let's Encrypt证书，确保防火墙开放80和443端口
2. **静态文件路径**: 生产环境需要先构建前端项目
3. **WebSocket**: 配置已包含WebSocket支持，无需额外配置
4. **健康检查**: 后端需要实现 `/health` 端点

## 相关链接

- [Caddy官方文档](https://caddyserver.com/docs/)
- [Caddyfile语法](https://caddyserver.com/docs/caddyfile)
