# Learning Sessions Feature

This document summarizes the Learning Sessions CRUD feature that now powers the demo backend.

## Data Model

| Field | Type | Notes |
|-------|------|-------|
| `id` | integer | Auto increment primary key |
| `title` | string(200) | Required |
| `description` | text | Optional |
| `status` | enum | `planned \| in_progress \| completed`, defaults to `planned` |
| `difficulty` | string(50) | Optional |
| `started_at` | datetime | ISO-8601, nullable |
| `completed_at` | datetime | ISO-8601, nullable |
| `created_at` | datetime | Stored in UTC, serialized as ISO-8601 `+00:00` |
| `updated_at` | datetime | Stored in UTC, serialized as ISO-8601 `+00:00` |

## Local Development (SQLite)

1. Copy `.env.example` to `.env` if you have not already.
2. Add the following line so the backend uses a local SQLite file:
   ```bash
   DATABASE_URL=sqlite:///learning_env.db
   ```
3. Run the migrations:
   ```bash
   alembic upgrade head
   ```
4. Start the backend (`python backend/app.py`). The SQLite file will be created in the repo root.

> When deploying (CI/CD or production), remove the `DATABASE_URL` override so the Postgres `POSTGRES_*` variables take effect, then run `alembic upgrade head` on the server.

## API Reference

All endpoints live under `/api/sessions`.

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/sessions/` | List sessions ordered by `created_at` desc |
| `POST` | `/api/sessions/` | Create a session |
| `GET` | `/api/sessions/<id>` | Fetch a session by id |
| `PATCH` | `/api/sessions/<id>` | Partial update |
| `DELETE` | `/api/sessions/<id>` | Delete a session |

### Request & Response Samples

```bash
curl -X POST http://localhost:8000/api/sessions/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Learn Flask","status":"planned"}'
```

Response:

```json
{
  "data": {
    "id": 1,
    "title": "Learn Flask",
    "status": "planned",
    "description": null,
    "difficulty": null,
    "started_at": null,
    "completed_at": null,
    "created_at": "2025-11-12T15:30:36.737687+00:00",
    "updated_at": "2025-11-12T15:30:36.737700+00:00"
  }
}
```

Update example:

```bash
curl -X PATCH http://localhost:8000/api/sessions/1 \
  -H "Content-Type: application/json" \
  -d '{"status":"in_progress","difficulty":"medium"}'
```

Delete example:

```bash
curl -X DELETE http://localhost:8000/api/sessions/1
```

## Testing

`pytest backend/tests -q` brings up a temporary SQLite database per test case. The suite covers creation, validation errors, listing order, updates, and deletions to ensure regressions are caught before pushes.
