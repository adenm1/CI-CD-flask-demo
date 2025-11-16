# Frontend Migration Checklist

This document captures the steps taken to migrate the CI/CD dashboard to the unified Svelte + Vite + Tailwind experience.

## Completed actions
- [x] Removed legacy `frontend/src`, `frontend/dist`, `frontend/node_modules`, and `frontend/svelte-frontend` artifacts while preserving the backend.
- [x] Scaffolded a fresh SvelteKit workspace with Tailwind CSS, TypeScript, and Vite.
- [x] Recreated the entire UI per the Apple/Linear-inspired spec (sidebar, navbar, cards, tables, charts, log drawer, auth/views).
- [x] Implemented API clients (`client.ts`, `auth.ts`, `pipelines.ts`, `deployments.ts`) that keep the backend contract unchanged and centralize `Authorization` headers.
- [x] Added Svelte stores for auth + pipelines with 10-second auto-refresh and localStorage token persistence.
- [x] Integrated `svelte-apexcharts` and reusable components for cards, charts, tables, and settings.
- [x] Added Playwright UI tests, component tests (Vitest + Testing Library), and a TypeScript mock API server for local development.
- [x] Documented environment variables via `.env.example` and configured Tailwind/Vite/SvelteKit builds.

## Next steps
- Run `npm install` inside `frontend/`.
- Start the backend (`cd backend && python app.py`) and frontend (`cd frontend && npm run dev`).
- Optionally run `npm run mock-api` + `npm run dev:mock` if the backend is unavailable.
- Execute quality gates before pushing: `npm run check`, `npm run test`, `npm run test:ui` (requires browsers installed), and `pytest backend/tests -q`.
