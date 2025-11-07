# CI/CD Flask Demo with HTTPS Support 🚀

Flask web application with Docker, Nginx reverse proxy, and automated CI/CD deployment via GitHub Actions. Supports both HTTP and HTTPS (Let's Encrypt).

---

## 🧠 Overview

This project demonstrates:
- Flask application with Docker containerization
- Nginx reverse proxy with SSL/TLS support
- Automated CI/CD deployment using GitHub Actions
- Let's Encrypt SSL certificate integration
- Health check endpoints for monitoring

---

## 🏗️ Project Structure

```

.
├── src/
│   └── api/
│       └── app.py          # Flask application
├── .github/
│   └── workflows/
│       └── deploy.yml      # CI/CD pipeline
├── docker-compose.yml      # Multi-container orchestration
├── Dockerfile              # Flask app container
├── nginx.conf              # Nginx configuration
├── setup-ssl.sh            # SSL certificate setup script
├── requirements.txt        # Python dependencies
└── README.md
```

---

## ⚙️ Quick Start

### Local Development (HTTP only)

```bash
# Build and start all services
docker compose up -d

# Check status
docker compose ps

# View logs
docker compose logs -f

# Stop services
docker compose down
```

Access the application:
- **Via Nginx**: http://localhost
- **Direct Flask**: http://localhost:8000
- **Health Check**: http://localhost/health

---

## 🔐 HTTPS Setup (Production)

### Prerequisites
1. Domain name pointing to your server
2. Ports 80 and 443 open in firewall

### Steps

1. **Update environment variables** (create `.env` file):
```bash
DOMAIN=your-domain.com
EMAIL=your-email@example.com
```

2. **Run SSL setup script**:
```bash
./setup-ssl.sh your-domain.com your-email@example.com
```

3. **Update nginx.conf**:
   - Uncomment the HTTPS server block
   - Replace `your-domain.com` with your actual domain

4. **Reload Nginx**:
```bash
docker compose exec nginx nginx -s reload
```

---

## 🚀 CI/CD Deployment

### GitHub Secrets Setup

Add these secrets to your GitHub repository (Settings → Secrets and variables → Actions):

```
SERVER_IP      # Your server IP address
SERVER_USER    # SSH username (e.g., ubuntu)
SSH_KEY        # Private SSH key for authentication
DOMAIN         # Your domain name (e.g., example.com)
EMAIL          # Your email for Let's Encrypt notifications
```

### Deployment Flow

1. Push to `main` branch
2. GitHub Actions triggers automatically
3. Code uploaded to server (`/opt/ci-cd-flask-demo`)
4. Services stopped gracefully
5. Environment variables configured
6. New Docker images built
7. Services started (Flask + Nginx)
8. **SSL certificate auto-obtained** (first deployment only)
9. **HTTPS auto-enabled** if certificate obtained
10. Health checks (HTTP/HTTPS)
11. Old images cleaned up

**Note**: On first deployment with `DOMAIN` and `EMAIL` secrets configured, the workflow will automatically:
- Obtain Let's Encrypt SSL certificate
- Enable HTTPS in Nginx
- Set up auto-renewal via Certbot

---

## 📋 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page |
| `/health` | GET | Health check (returns 200 OK) |

---

## 🛠️ Requirements

- Docker Engine 24+
- Docker Compose V2
- Python 3.11+
- GitHub account (for CI/CD)

---

## 🔧 Configuration Files

### docker-compose.yml
- **web**: Flask application (Python + Gunicorn)
- **nginx**: Reverse proxy with SSL support
- **certbot**: SSL certificate management (auto-renewal)

### nginx.conf
- HTTP server on port 80
- HTTPS server on port 443 (when configured)
- Proxy headers for real IP forwarding
- Let's Encrypt ACME challenge support

---

## 📝 Maintenance

### SSL Certificate Renewal
Certificates auto-renew via Certbot container (every 12 hours check).

### Manual renewal:
```bash
docker compose run --rm certbot renew
docker compose exec nginx nginx -s reload
```

### View logs:
```bash
# All services
docker compose logs

# Specific service
docker compose logs nginx
docker compose logs web
docker compose logs certbot
```

---

## 🧰 Troubleshooting

**Issue**: HTTPS not working after setup
- Verify domain DNS points to server IP
- Check ports 80/443 are open
- Review nginx logs: `docker logs nginx-proxy`

**Issue**: Health check failed
- Check Flask app logs: `docker logs flask-app`
- Verify containers running: `docker compose ps`
- Test direct access: `curl http://localhost:8000/health`

---

## 📄 License

MIT