# Pre-Push Checklist

## 必须完成的步骤

### 1. 清理旧文件
```bash
# 删除废弃的 src/ 目录
rm -rf src/

# 删除临时文件
rm -rf .trash/
```

### 2. 创建环境文件（服务器上会需要）
```bash
# 确保 .env.example 存在
cat .env.example
```

### 3. 本地测试 Docker 构建
```bash
# 测试构建（可选但建议）
docker compose build

# 如果构建成功，清理
docker compose down
docker system prune -f
```

### 4. 检查 Git 状态
```bash
git status

# 应该看到:
# - backend/ (新目录)
# - frontend/ (新目录)
# - .env.example (新文件)
# - 修改的配置文件
```

### 5. 提交所有更改
```bash
# 添加所有新文件和更改
git add .

# 创建提交
git commit -m "refactor: restructure project following Apple standards

- Reorganize backend into modular architecture (backend/)
- Separate frontend into standalone TypeScript project (frontend/)
- Implement application factory pattern with config management
- Add comprehensive error handling and logging
- Fix Dockerfile typo (PYTHONDONTWRITEBYTECODE)
- Update Docker and nginx configurations
- Add extensive documentation (Claude.md)
- Improve security (non-root Docker user, .env management)"
```

### 6. Push 到远程
```bash
git push origin main
```

## CI/CD 会执行的操作

1. ✅ 上传代码到服务器 `/opt/ci-cd-flask-demo`
2. ✅ 停止旧服务并释放端口 80/443
3. ✅ 生成自签名 SSL 证书（如果不存在）
4. ✅ 构建 Docker 镜像
5. ✅ 启动服务（backend + nginx）
6. ✅ 健康检查（HTTP/HTTPS）
7. ✅ 清理旧镜像

## 预期结果

- **Backend**: http://YOUR_SERVER_IP:8000
- **Frontend + API (via Nginx)**: http://YOUR_SERVER_IP
- **HTTPS**: https://YOUR_SERVER_IP (自签名证书，浏览器会警告)
- **Health Check**: http://YOUR_SERVER_IP/health

## 可能的问题

### 问题 1: Backend 服务启动失败
**原因**:
- 代码错误
- 依赖缺失
- 环境变量配置问题

**解决**: 查看 GitHub Actions 日志中的 `docker compose logs backend`

### 问题 2: Nginx 无法代理
**原因**:
- Backend 服务未启动
- 网络配置问题

**解决**: 检查服务间网络连接

### 问题 3: 端口被占用
**原因**:
- 旧服务未正确停止

**解决**: CI/CD 会自动清理，如需手动：
```bash
ssh YOUR_SERVER
sudo fuser -k 80/tcp
sudo fuser -k 443/tcp
```

## 验证部署成功

登录服务器检查：
```bash
ssh YOUR_SERVER_USER@YOUR_SERVER_IP

cd /opt/ci-cd-flask-demo

# 检查服务状态
docker compose ps

# 查看日志
docker compose logs -f

# 测试 API
curl http://localhost/health
curl http://localhost/api/hello
```

## 回滚方案

如果部署失败，在服务器上执行：
```bash
cd /opt/ci-cd-flask-demo

# 停止服务
docker compose down

# 回退到之前的代码版本（如果你有备份）
# 或者等待修复后重新 push
```

---
