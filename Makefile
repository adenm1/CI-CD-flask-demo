.PHONY: help install dev test lint format clean build deploy

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install all dependencies
	@echo "📦 Installing backend dependencies..."
	pip install -r requirements.txt
	@echo "📦 Installing frontend dependencies..."
	cd frontend && npm install
	@echo "✅ Dependencies installed!"

install-dev: install ## Install development dependencies including pre-commit
	pip install pre-commit
	pre-commit install
	@echo "✅ Development environment ready!"

dev: ## Start development environment
	@echo "🚀 Starting development services..."
	docker compose up --build

dev-backend: ## Start only backend for development
	@echo "🚀 Starting backend development server..."
	cd backend && python app.py

dev-frontend: ## Start only frontend for development
	@echo "🚀 Starting frontend development server..."
	cd frontend && npm run dev

test: ## Run all tests
	@echo "🧪 Running backend tests..."
	pytest backend/tests/ -v --cov=backend --cov-report=html --cov-report=term
	@echo "🧪 Running frontend tests..."
	cd frontend && npm test

test-unit: ## Run unit tests only
	pytest backend/tests/unit/ -v

test-integration: ## Run integration tests only
	pytest backend/tests/integration/ -v

test-watch: ## Run tests in watch mode
	pytest backend/tests/ -v --cov=backend -f

lint: ## Run linters
	@echo "🔍 Running Python linters..."
	flake8 backend/ --max-line-length=120 --exclude=__pycache__,migrations
	@echo "🔍 Running frontend linters..."
	cd frontend && npm run check

format: ## Format code
	@echo "✨ Formatting Python code..."
	black backend/
	@echo "✨ Checking frontend code..."
	cd frontend && npm run check

security: ## Run security checks
	@echo "🔒 Running security scans..."
	bandit -r backend/ -ll
	pip-audit
	@echo "✅ Security check complete!"

clean: ## Clean up generated files
	@echo "🧹 Cleaning up..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache htmlcov .coverage
	rm -rf frontend/dist frontend/.svelte-kit
	@echo "✅ Cleanup complete!"

build: ## Build Docker images
	@echo "🏗️  Building Docker images..."
	docker compose build
	@echo "✅ Build complete!"

build-frontend: ## Build frontend for production
	@echo "🏗️  Building frontend..."
	cd frontend && npm run build
	@echo "✅ Frontend build complete!"

up: ## Start all services
	docker compose up -d

down: ## Stop all services
	docker compose down

logs: ## View logs
	docker compose logs -f

ps: ## Show running containers
	docker compose ps

deploy: ## Deploy to production (via CI/CD)
	@echo "🚀 Triggering deployment..."
	@echo "⚠️  Deployment should be done through CI/CD pipeline"
	@echo "Push to main branch to trigger automated deployment"

db-migrate: ## Run database migrations
	@echo "🗂️  Running database migrations..."
	docker compose run --rm backend alembic upgrade head
	@echo "✅ Migrations complete!"

db-rollback: ## Rollback last migration
	@echo "⏪ Rolling back last migration..."
	docker compose run --rm backend alembic downgrade -1

db-reset: ## Reset database (WARNING: destroys all data)
	@echo "⚠️  This will destroy all data!"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker compose down -v; \
		docker compose up -d postgres; \
		sleep 5; \
		make db-migrate; \
	fi

k8s-deploy: ## Deploy to Kubernetes
	@echo "☸️  Deploying to Kubernetes..."
	kubectl apply -f k8s/namespace.yaml
	kubectl apply -f k8s/configmap.yaml
	kubectl apply -f k8s/postgres-statefulset.yaml
	kubectl apply -f k8s/redis-deployment.yaml
	kubectl apply -f k8s/backend-deployment.yaml
	@echo "✅ Kubernetes deployment complete!"

k8s-delete: ## Delete Kubernetes resources
	kubectl delete -f k8s/backend-deployment.yaml
	kubectl delete -f k8s/redis-deployment.yaml
	kubectl delete -f k8s/postgres-statefulset.yaml
	kubectl delete -f k8s/configmap.yaml
	kubectl delete -f k8s/namespace.yaml

monitoring: ## Open monitoring dashboards
	@echo "📊 Opening monitoring dashboards..."
	@echo "Prometheus: http://localhost:9090"
	@echo "Grafana: http://localhost:3000 (admin/admin)"
	@echo "API Docs: http://localhost:8000/api/docs/"

shell-backend: ## Open shell in backend container
	docker compose exec backend /bin/bash

shell-db: ## Open PostgreSQL shell
	docker compose exec postgres psql -U postgres -d learning_env

shell-redis: ## Open Redis CLI
	docker compose exec redis redis-cli

health-check: ## Check health of all services
	@echo "🏥 Checking service health..."
	@curl -f http://localhost:8000/health || echo "❌ Backend unhealthy"
	@curl -f http://localhost:9090/-/healthy || echo "❌ Prometheus unhealthy"
	@curl -f http://localhost:3000/api/health || echo "❌ Grafana unhealthy"
	@echo "✅ Health check complete!"

ci: lint test security ## Run CI pipeline locally
	@echo "✅ CI pipeline complete!"
