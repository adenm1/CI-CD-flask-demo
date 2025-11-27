# Flask CI/CD Demo

> Production-ready full-stack application with Flask backend, Svelte frontend, comprehensive monitoring, and enterprise-grade security.

**Version**: 2.0.0 | **Status**: Production Ready

[![Security Scan](https://github.com/yourusername/CI-CD-flask-demo/workflows/Security%20Scanning/badge.svg)](https://github.com/yourusername/CI-CD-flask-demo/actions)
[![Tests](https://github.com/yourusername/CI-CD-flask-demo/workflows/Tests/badge.svg)](https://github.com/yourusername/CI-CD-flask-demo/actions)

---

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/yourusername/CI-CD-flask-demo.git
cd CI-CD-flask-demo

# Start all services with one command
make dev

# Or with Docker Compose
docker compose up -d
```

**Access Points:**
- 🌐 Frontend: http://localhost
- 🔌 API: http://localhost:8000
- 📊 API Docs: http://localhost:8000/api/docs/
- 📈 Grafana: http://localhost:3000
- 🔍 Prometheus: http://localhost:9090

---

## ✨ Features

### Backend
- ⚡ **Flask 3.1** with application factory pattern
- 🗄️ **PostgreSQL** with SQLAlchemy ORM and Alembic migrations
- 🔄 **Redis** for caching and sessions
- 🔒 **Security**: Rate limiting, security headers, JWT authentication
- 📊 **Monitoring**: Prometheus metrics, Sentry error tracking
- 📝 **API Docs**: Auto-generated Swagger/OpenAPI documentation

### Frontend
- 🎨 **Svelte 5** with runes for fine-grained reactivity
- 📱 **SvelteKit 2** with server-side rendering support
- 🎯 **TypeScript** for type safety
- 🎨 **TailwindCSS** for modern styling

### DevOps
- 🐳 **Docker** & **Docker Compose** for containerization
- ☸️ **Kubernetes** manifests for production deployment
- 🔄 **CI/CD** with GitHub Actions (security scanning, performance testing)
- 📊 **Monitoring Stack**: Prometheus + Grafana dashboards
- 🛠️ **Developer Tools**: Makefile, pre-commit hooks

### Security
- 🔐 JWT authentication with MFA (TOTP)
- 🛡️ Rate limiting and security headers
- 🔍 Automated security scanning (Bandit, Trivy, CodeQL, Gitleaks)
- 📝 Audit logging with cryptographic signatures
- 🔒 Approval-based registration workflow

---

## 📚 Documentation

### Getting Started
- **[Installation Guide](docs/INSTALLATION.md)** - Detailed setup instructions
- **[Quick Start](docs/QUICK_START.md)** - Get running in 5 minutes
- **[Configuration Guide](docs/CONFIGURATION.md)** - Environment variables and settings

### Development
- **[Development Guide](docs/DEVELOPMENT.md)** - Local development workflow
- **[Testing Guide](docs/TESTING.md)** - Running and writing tests
- **[Svelte 5 Migration](docs/SVELTE5_MIGRATION.md)** - Upgrading to Svelte 5

### Architecture
- **[Project Structure](docs/PROJECT_STRUCTURE.md)** - Directory layout and organization
- **[API Documentation](docs/API.md)** - Endpoint reference
- **[Claude.md](docs/Claude.md)** - AI collaboration changelog (Single Source of Truth)

### Deployment
- **[Docker Deployment](docs/DOCKER.md)** - Containerized deployment
- **[Kubernetes Deployment](k8s/README.md)** - Production Kubernetes setup
- **[CI/CD Guide](docs/CICD.md)** - Automated deployment pipeline

### Operations
- **[Monitoring Guide](docs/MONITORING.md)** - Prometheus and Grafana setup
- **[Security Guide](docs/SECURITY.md)** - Security best practices
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions

### Planning
- **[Improvements Summary](docs/IMPROVEMENTS.md)** - What's new in v2.0
- **[TODO & Roadmap](docs/TODO.md)** - Future plans and long-term innovations
- **[Implementation Summary](docs/IMPLEMENTATION_SUMMARY.md)** - v2.0 implementation details

---

## 🏗️ Architecture

```
┌─────────────────┐
│   Nginx Proxy   │  ← HTTPS, Static Files, Rate Limiting
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼───┐  ┌─▼─────┐
│ Frontend│  │Backend│  ← Flask API, Prometheus Metrics
│ Svelte 5│  │Flask  │
└─────────┘  └──┬────┘
                │
        ┌───────┼───────┐
        │       │       │
    ┌───▼──┐ ┌─▼───┐ ┌▼────────┐
    │Redis │ │Postgres│ │Prometheus│
    │Cache │ │  DB  │ │ +Grafana │
    └──────┘ └──────┘ └─────────┘
```

---

## 🛠️ Developer Commands

We provide a comprehensive Makefile for common tasks:

```bash
make help            # Show all available commands
make install-dev     # Install with pre-commit hooks
make dev             # Start development environment
make test            # Run all tests with coverage
make lint            # Run code linters
make format          # Format code (Black, isort)
make security        # Run security checks
make build           # Build Docker images
make monitoring      # Open monitoring dashboards
```

**Full command reference**: Run `make help`

---

## 🔒 Security Features

- **Rate Limiting**: Prevent DoS attacks (configurable per route)
- **Security Headers**: CSP, HSTS, X-Frame-Options (OWASP compliant)
- **Authentication**: JWT with TOTP MFA support
- **Audit Logging**: Cryptographically signed audit trail
- **Automated Scanning**: 4 types of security scans in CI/CD
- **Secrets Detection**: Prevents secrets from being committed
- **Container Scanning**: Trivy scans Docker images for vulnerabilities

---

## 📊 Monitoring & Observability

- **Prometheus**: Collects application metrics automatically
- **Grafana**: Pre-configured dashboards for visualization
- **Sentry**: Error tracking with stack traces (optional)
- **Structured Logging**: JSON logs for easy parsing
- **Health Checks**: Kubernetes-ready liveness/readiness probes

**Access**: http://localhost:3000 (Grafana) | http://localhost:9090 (Prometheus)

---

## ☸️ Kubernetes Ready

Production-ready Kubernetes manifests included:

```bash
# Deploy to Kubernetes
make k8s-deploy

# Or manually
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/backend-deployment.yaml
# ... (see k8s/README.md)
```

**Features:**
- Horizontal Pod Autoscaler (2-10 replicas)
- StatefulSet for PostgreSQL
- Ingress with TLS support
- Resource limits and requests
- Health checks configured

---

## 🧪 Testing

```bash
# Run all tests
make test

# Run specific test types
make test-unit           # Unit tests only
make test-integration    # Integration tests only

# Security testing
make security            # Security scans

# Performance testing
cd frontend && npm run test:ui  # Playwright UI tests
```

**Test Coverage**: Foundation for 80%+ coverage

---

## 🚢 Deployment

### Option 1: Docker Compose (Development/Staging)
```bash
docker compose up -d
```

### Option 2: Kubernetes (Production)
```bash
make k8s-deploy
```

### Option 3: CI/CD (Automated)
Push to `main` branch → GitHub Actions → Auto-deploy

**See**: [CI/CD Guide](docs/CICD.md)

---

## 📦 Technology Stack

| Category | Technology |
|----------|-----------|
| **Backend** | Flask 3.1, SQLAlchemy, Alembic, Gunicorn |
| **Frontend** | Svelte 5, SvelteKit 2, TypeScript, TailwindCSS |
| **Database** | PostgreSQL 16, Redis 7 |
| **Monitoring** | Prometheus, Grafana, Sentry |
| **Security** | Flask-Limiter, Flask-Talisman, PyOTP, Cryptography |
| **Testing** | Pytest, Vitest, Playwright, Locust |
| **DevOps** | Docker, Kubernetes, GitHub Actions |

---

## 🤝 Contributing

1. Read the [Development Guide](docs/DEVELOPMENT.md)
2. Check the [TODO](docs/TODO.md) for planned features
3. Follow code quality standards (pre-commit hooks enforce this)
4. Write tests for new features
5. Update documentation

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file

---

## 👤 Author

**Si Ying Liu**

---

## 🙏 Acknowledgments

Built with best practices from:
- Flask official documentation
- Svelte 5 modern patterns
- Kubernetes production guides
- OWASP security standards
- Twelve-Factor App methodology

---

## 📞 Support

- **Documentation**: See [docs/](docs/) folder
- **Issues**: [GitHub Issues](https://github.com/yourusername/CI-CD-flask-demo/issues)
- **Troubleshooting**: [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)

---

**⭐ Star this repo if you find it useful!**
