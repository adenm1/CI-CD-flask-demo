# Project Structure Guide

This document captures the full layout of the CI-CD-flask-demo repository so contributors can quickly locate backend,
frontend, and infra artifacts.

## Root

```
CI-CD-flask-demo/
├── backend/                # Flask API (app factory + blueprints)
├── frontend/               # SvelteKit dashboard
├── docs/                   # Documentation
├── scripts/                # Automation scripts (e.g., prepare-push)
├── docker-compose.yml      # Docker topology for local/server
├── Dockerfile              # Backend image
├── nginx.conf              # Nginx reverse proxy
├── requirements.txt        # Backend dependencies
└── README.md               # Project overview
```

## Backend (`backend/`)

```
backend/
├── api/
│   ├── routes/             # Blueprints (auth, pipelines, sessions…)
│   ├── services/           # Business logic layer
│   ├── models/             # SQLAlchemy models（admin_users、registration_requests、approval_keys、audit_events…）
│   └── middleware/         # Custom middleware (reserved)
├── config/
│   └── settings.py         # Environment-aware configuration
├── utils/
│   ├── db.py               # DB bootstrap & session factory
│   ├── passwords.py        # Password hashing with pepper
│   └── security.py         # Token helpers + default admin
├── tests/
│   └── test_*.py           # Pytest suites
└── app.py                  # Gunicorn entry (backend.app:app)
```

Guidelines:

- Keep blueprints focused on HTTP orchestration; heavy logic lives in `services/`.
- Register new blueprints inside `api/routes/__init__.py` and pair them with tests under `backend/tests`.
- Store config exclusively in `backend.config.settings`.

## Frontend (`frontend/`)

```
frontend/
├── src/
│   ├── lib/
│   │   ├── components/     # UI components (Card, PipelineTable…)
│   │   ├── stores/         # Svelte stores (auth, pipelines)
│   │   └── api/            # Fetch client + contracts
│   ├── routes/             # Pages (+layout, login, dashboards)
│   ├── assets/             # Global styles / Tailwind config
│   └── app.html/app.css    # Entry hooks
├── package.json            # SvelteKit dependencies
└── tests/                  # Playwright/Vitest (extensible)
```

## Infra & automation

- `docker-compose.yml`: Postgres + Backend + Nginx.
- `Dockerfile`: multi-stage build, final `backend.app:app` served by Gunicorn.
- `.github/workflows/deploy.yml`: CI/CD workflow.
- `scripts/prepare-push.sh`: local pre-flight checks.

## Documentation

- `docs/PROJECT_STRUCTURE.md` (this file) — structure index.
- `README.md` — overview & quick start.

Keep this doc updated whenever new modules are added so the structure remains transparent.
