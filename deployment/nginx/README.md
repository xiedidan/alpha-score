# Nginx部署指南

## 简介

本目录包含Alpha-Score项目的Nginx反向代理配置，提供高性能的HTTP服务、静态文件托管和负载均衡。

## 文件说明

- `nginx.conf` - Nginx主配置文件

## 功能特性

1. **反向代理**
   - API请求代理到后端FastAPI
   - WebSocket长连接支持
   - 健康检查

2. **静态文件���管**
   - 前端静态资源服务
   - SPA路由支持
   - 智能缓存策略

3. **SSL/TLS**
   - Let's Encrypt证书支持
   - TLS 1.2/1.3
   - HSTS安全头

4. **安全增强**
   - CSP、XSS保护
   - 请求大小限制
   - 隐藏文件保护

5. **性能优化**
   - Gzip压缩
   - 静态资源缓存
   - 连接保持
   - 负载均衡

## 快速开始

### 安装Nginx

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install nginx

# CentOS/RHEL
sudo yum install nginx

# 验证安装
nginx -v
```

### 部署配置

```bash
# 1. 备份原配置
sudo cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bak

# 2. 复制配置文件
sudo cp deployment/nginx/nginx.conf /etc/nginx/sites-available/alpha-score

# 3. 创建软链接
sudo ln -s /etc/nginx/sites-available/alpha-score /etc/nginx/sites-enabled/

# 4. 测试配置
sudo nginx -t

# 5. 重载配置
sudo systemctl reload nginx
```

## 详细配置

### 1. 开发环境

开发环境配置在文件底部：

```nginx
server {
    listen 80;
    server_name localhost 127.0.0.1;

    # API代理到FastAPI
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
    }

    # 前端代理到Vite开发服务器
    location / {
        proxy_pass http://127.0.0.1:5173;
    }
}
```

访问: http://localhost

### 2. 生产环境

#### 步骤1: 修改域名

```nginx
# 将 alpha-score.example.com 改为实际域名
server_name your-domain.com;
```

#### 步骤2: 构建前端

```bash
cd /home/xd/project/alpha-score/frontend
npm run build

# 复制到nginx目录
sudo mkdir -p /var/www/alpha-score
sudo cp -r dist /var/www/alpha-score/
```

#### 步骤3: 配置SSL证书

使用Let's Encrypt（推荐）：

```bash
# 安装certbot
sudo apt install certbot python3-certbot-nginx

# 申请证书
sudo certbot --nginx -d your-domain.com

# 或手动配置
sudo certbot certonly --webroot -w /var/www/certbot -d your-domain.com

# 自动续期
sudo crontab -e
# 添加: 0 3 * * * certbot renew --quiet
```

#### 步骤4: 启动服务

```bash
# 测试配置
sudo nginx -t

# 启动Nginx
sudo systemctl start nginx

# 开机自启
sudo systemctl enable nginx
```

### 3. 负载均衡（多Worker）

如果运行多个后端实例：

```nginx
upstream alpha_backend {
    # 轮询
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;

    # 或使用IP哈希（保持会话）
    # ip_hash;

    # 或使用最少连接
    # least_conn;
}
```

启动多个后端：

```bash
# 端口8000
cd /home/xd/project/alpha-score/backend
./venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 &

# 端口8001
./venv/bin/uvicorn main:app --host 0.0.0.0 --port 8001 &

# 端口8002
./venv/bin/uvicorn main:app --host 0.0.0.0 --port 8002 &
```

### 4. 缓存配置

添加缓存目录：

```nginx
# 在http块中添加
proxy_cache_path /var/cache/nginx/alpha levels=1:2 keys_zone=alpha_cache:10m max_size=1g inactive=60m;

# 在location /api/中添加
proxy_cache alpha_cache;
proxy_cache_valid 200 5m;
proxy_cache_bypass $http_cache_control;
add_header X-Cache-Status $upstream_cache_status;
```

### 5. 日志配置

自定义日志格式：

```nginx
# 在http块中添加
log_format alpha_log '$remote_addr - $remote_user [$time_local] '
                     '"$request" $status $body_bytes_sent '
                     '"$http_referer" "$http_user_agent" '
                     'rt=$request_time uct="$upstream_connect_time" '
                     'uht="$upstream_header_time" urt="$upstream_response_time"';

# 使用自定义格式
access_log /var/log/nginx/alpha-score-access.log alpha_log;
```

## 常用命令

### 服务管理

```bash
# 启动
sudo systemctl start nginx

# 停止
sudo systemctl stop nginx

# 重启
sudo systemctl restart nginx

# 重载配置（无缝）
sudo systemctl reload nginx

# 查看状态
sudo systemctl status nginx
```

### 配置测试

```bash
# 测试配置语法
sudo nginx -t

# 测试并显示配置
sudo nginx -T

# 查看编译参数
nginx -V
```

### 日志查看

```bash
# 实时访问日志
sudo tail -f /var/log/nginx/alpha-score-access.log

# 实时错误日志
sudo tail -f /var/log/nginx/alpha-score-error.log

# 查看最近错误
sudo tail -100 /var/log/nginx/error.log
```

## 故障排查

### 1. 502 Bad Gateway

**原因**: 后端服务未启动或端口错误

```bash
# 检查后端是否运行
sudo lsof -i:8000

# 启动后端
cd /home/xd/project/alpha-score/backend
./venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000

# 检查防火墙
sudo ufw status
sudo ufw allow 8000
```

### 2. 403 Forbidden

**原因**: 文件权限或目录索引问题

```bash
# 检查静态文件权限
ls -la /var/www/alpha-score/dist

# 修改权限
sudo chown -R www-data:www-data /var/www/alpha-score
sudo chmod -R 755 /var/www/alpha-score

# 检查SELinux（CentOS）
sudo setenforce 0
```

### 3. 504 Gateway Timeout

**原因**: 后端响应超时

```nginx
# 增���超时时间
proxy_connect_timeout 120s;
proxy_send_timeout 120s;
proxy_read_timeout 120s;
```

### 4. WebSocket连接失败

**检查配置**:

```nginx
location /ws/ {
    proxy_pass http://alpha_backend;

    # 这两行必须有
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";

    # 增加超时
    proxy_read_timeout 86400;
}
```

### 5. SSL证书问题

```bash
# 检查证书
sudo certbot certificates

# 续期证书
sudo certbot renew --dry-run
sudo certbot renew

# 强制续期
sudo certbot renew --force-renewal
```

## 性能优化

### 1. Worker配置

```nginx
# 在主配置文件 /etc/nginx/nginx.conf 中
worker_processes auto;  # CPU核心数
worker_connections 2048;  # 每个worker的连接数
```

### 2. Gzip压缩

```nginx
gzip on;
gzip_vary on;
gzip_proxied any;
gzip_comp_level 6;
gzip_types text/plain text/css text/xml text/javascript
           application/json application/javascript application/xml+rss
           application/rss+xml font/truetype font/opentype
           application/vnd.ms-fontobject image/svg+xml;
gzip_disable "msie6";
```

### 3. 文件缓存

```nginx
# 打开文件缓存
open_file_cache max=1000 inactive=20s;
open_file_cache_valid 30s;
open_file_cache_min_uses 2;
open_file_cache_errors on;
```

### 4. 连接优化

```nginx
# 保持连接
keepalive_timeout 65;
keepalive_requests 100;

# 客户端缓冲
client_body_buffer_size 128k;
client_header_buffer_size 1k;
large_client_header_buffers 4 4k;
```

## 监控和日志分析

### 使用GoAccess分析日志

```bash
# 安装GoAccess
sudo apt install goaccess

# 实时分析
sudo goaccess /var/log/nginx/alpha-score-access.log --log-format=COMBINED

# 生成HTML报告
sudo goaccess /var/log/nginx/alpha-score-access.log \
    --log-format=COMBINED \
    -o /var/www/html/report.html
```

### Nginx状态监控

```nginx
# 添加状态页面
location /nginx_status {
    stub_status on;
    access_log off;
    allow 127.0.0.1;
    deny all;
}
```

访��: http://localhost/nginx_status

## 安全建议

1. **定期更新Nginx**
```bash
sudo apt update && sudo apt upgrade nginx
```

2. **限制请求频率**
```nginx
# 在http块中
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;

# 在location中
limit_req zone=api_limit burst=20 nodelay;
```

3. **隐藏版本号**
```nginx
http {
    server_tokens off;
}
```

4. **IP黑名单**
```nginx
# 创建黑名单文件
echo "deny 192.168.1.100;" | sudo tee /etc/nginx/blockips.conf

# 在server块中包含
include /etc/nginx/blockips.conf;
```

## 相关链接

- [Nginx官方文档](https://nginx.org/en/docs/)
- [Let's Encrypt](https://letsencrypt.org/)
- [Mozilla SSL配置生成器](https://ssl-config.mozilla.org/)
- [Nginx配置最佳实践](https://www.nginx.com/blog/tuning-nginx/)
