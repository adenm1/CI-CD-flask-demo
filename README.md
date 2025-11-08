# Flask CI/CD Demo

> Modern full-stack web application with Flask backend and TypeScript frontend

Production-ready web application demonstrating best practices in software architecture, containerization, and CI/CD deployment.

---

## Features

- **Backend**: Flask 3.1 with application factory pattern, modular architecture, and comprehensive error handling
- **Frontend**: TypeScript + Vite with type-safe API client and modern CSS
- **Infrastructure**: Docker containerization with Nginx reverse proxy
- **Development**: Environment-based configuration, hot-reload, and debugging
- **Production**: Optimized builds, health checks, and SSL/TLS support
- **Code Quality**: Apple engineering standards, comprehensive documentation

---

## Project Structure

```
CI-CD-flask-demo/
├── backend/                    # Flask backend (Python 3.11)
│   ├── api/                   # Application logic
│   │   ├── routes/           # API endpoints (blueprints)
│   │   ├── models/           # Data models
│   │   ├── services/         # Business logic
│   │   └── middleware/       # Custom middleware
│   ├── config/               # Configuration management
│   ├── utils/                # Utility functions
│   └── app.py                # Application entry point
│
├── frontend/                  # TypeScript + Vite frontend
│   ├── src/
│   │   ├── assets/          # Static assets (CSS, images)
│   │   ├── components/      # UI components
│   │   ├── services/        # API client
│   │   ├── types/           # TypeScript definitions
│   │   └── main.ts          # Entry point
│   ├── vite.config.ts       # Vite configuration
│   └── tsconfig.json        # TypeScript configuration
│
├── Dockerfile               # Backend container image
├── docker-compose.yml       # Multi-container orchestration
├── requirements.txt         # Python dependencies
├── .env.example            # Environment template
└── Claude.md               # Comprehensive documentation
```

---

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+ (for frontend development)
- Docker & Docker Compose (for containerized deployment)

### Option 1: Local Development

#### Backend Development
```bash
# Navigate to project root
cd CI-CD-flask-demo

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
export FLASK_ENV=development

# Run backend
cd backend && python app.py
```

Backend will run at: http://localhost:8000

#### Frontend Development
```bash
# Open new terminal, navigate to frontend
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will run at: http://localhost:5173 (with API proxy to backend)

### Option 2: Docker (Recommended for Production)

```bash
# Set up environment
cp .env.example .env
# Edit .env with your configuration

# Build and start all services
docker compose up -d --build

# Check status
docker compose ps

# View logs
docker compose logs -f

# Stop services
docker compose down
```

Access points:
- **Frontend (via Nginx)**: http://localhost
- **Backend API**: http://localhost:8000
- **Health Check**: http://localhost/health or http://localhost:8000/health

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

## API Endpoints

### Health & Status
| Endpoint | Method | Description | Response |
|----------|--------|-------------|----------|
| `/` | GET | API information | JSON with version, endpoints |
| `/health` | GET | Health check | `{"status": "healthy", ...}` |

### Business Logic
| Endpoint | Method | Description | Response |
|----------|--------|-------------|----------|
| `/api/hello` | GET | Hello message | `{"message": "...", "author": "...", ...}` |
| `/api/status` | GET | System status | `{"status": "...", "environment": "...", ...}` |

---

## Configuration

### Environment Variables

Create a `.env` file from `.env.example`:

```bash
# Application Environment
FLASK_ENV=development  # Options: development, production, testing

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Security
SECRET_KEY=your-secret-key-change-in-production

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Logging
LOG_LEVEL=INFO  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
```

---

## Development

### Backend Structure

```python
# Import example - using application factory pattern
from backend.api import create_app

app = create_app('development')
```

**Key Modules**:
- `backend/api/routes/` - Blueprint-based route handlers
- `backend/config/settings.py` - Environment-based configuration
- `backend/api/__init__.py` - Application factory with error handling

### Frontend Structure

```typescript
// Import examples - using path aliases
import { apiService } from '@/services';
import type { HelloResponse } from '@/types';

// Type-safe API calls
const response = await apiService.getHello();
```

**Key Features**:
- Type-safe API client with error handling
- Path aliases (`@/`, `@components/`, `@services/`)
- Apple-inspired design system with CSS variables
- Vite for fast development and optimized builds

### Code Quality Standards

This project follows Apple engineering standards:
- Modular architecture with clear separation of concerns
- Comprehensive error handling and logging
- Type safety (TypeScript frontend, type hints in Python)
- Environment-based configuration
- Security best practices (non-root Docker user, input validation)
- Extensive documentation (see `Claude.md`)

---

## Building for Production

### Frontend Build
```bash
cd frontend
npm run build
# Output: frontend/dist/
```

### Backend Docker Image
```bash
# Build image
docker build -t flask-backend .

# Run container
docker run -p 8000:8000 --env-file .env flask-backend
```

### Full Stack Deployment
```bash
# Build frontend
cd frontend && npm run build && cd ..

# Start all services
docker compose up -d --build

# Nginx will serve frontend static files from frontend/dist/
# and proxy /api requests to backend
```

---

## Maintenance

### View Logs
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs backend
docker compose logs nginx
```

### Update Dependencies
```bash
# Backend
pip list --outdated
pip install --upgrade <package>
pip freeze > requirements.txt

# Frontend
cd frontend
npm outdated
npm update
```

---

## Troubleshooting

### Backend Issues

**Import Error: `No module named 'backend'`**
```bash
# Solution: Run from project root with PYTHONPATH
cd CI-CD-flask-demo
PYTHONPATH=. python backend/app.py
```

**Port 8000 already in use**
```bash
# Find and kill process
lsof -i :8000
kill -9 <PID>

# Or change port in .env
PORT=8001
```

**Health check fails**
```bash
# Check logs
docker compose logs backend

# Test directly
curl http://localhost:8000/health
```

### Frontend Issues

**CORS errors**
- Add frontend URL to `CORS_ORIGINS` in `.env`

**TypeScript errors**
```bash
cd frontend
npm run type-check
```

**Module not found with @ imports**
- Check `vite.config.ts` and `tsconfig.json` path configurations match

### Docker Issues

**Container exits immediately**
```bash
# View logs
docker logs flask-backend

# Run interactively
docker run -it --rm flask-backend /bin/bash
```

---

## Documentation

- **Claude.md** - Comprehensive development documentation (Single Source of Truth)
- **API Documentation** - See API Endpoints section above
- **Configuration** - See `.env.example` for all available options

---

## Author

**Si Ying Liu**

---

## License

MIT