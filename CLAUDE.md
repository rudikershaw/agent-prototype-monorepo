# CLAUDE.md

## Project Overview
This is an AI-powered chat application built as a technical assignment for Owkin. The app features a conversational interface where users can ask questions about biotech data (genes, cancer indications, expression values). The backend delegates to an OpenAI-compatible LLM endpoint (default: local LM Studio) using `pydantic_ai` for agent management and streaming responses.

## Tech Stack
- **Backend**: Python 3.12+, FastAPI (`fastapi[standard]`), `pydantic_ai`, `httpx2`, Pydantic
- **Frontend**: React 19, React Router v7 (SSR), Vite, Tailwind CSS 4, TypeScript, `@assistant-ui/react`
- **Tooling**: `uv` (workspace), `nox` (automation), `ruff`, `mypy`, `bandit`, `pip-audit`, `pytest`, Biome

Use `uv run nox -l` and `uv run noc -s ${SESSION}` over manual commands to the various tools.

## Repository Structure
- `backend/` — FastAPI application
  - `src/api/main.py` — App entry point, router registration, CORS setup
  - `src/api/controller/chat.py` — `/chat` POST endpoint (streaming)
  - `src/api/controller/health.py` — `/` GET health check endpoint
  - `src/api/service/inference.py` — `InferenceService` wrapping a `pydantic_ai.Agent` with an OpenAI-compatible model
  - `src/api/config/` — `InferenceConfig` (model name, host URL) and CORS configuration
- `frontend/` — React application
  - `app/routes/` — Route definitions: home (chat), assistant (standalone chat page), health status, API proxy (`api/chat`)
  - `app/components/assistant-ui/` — Custom Assistant UI components (thread, markdown rendering, reasoning panels, tool fallbacks)
  - `app/utils/chat-model-adapter.ts` — ChatModelAdapter that serializes messages to the backend `/chat` endpoint
  - `app/config.ts` — API URL configuration (`VITE_API_URL`)
- `technical-test/` — Assignment materials (data CSV, spec document)

## Development Workflow

Prefer using `nox` commands using `uv` over manual program calls.

### Backend (Python)
- **Dependency Management**: `uv sync` (workspace-level). All Python commands should use `uv run`.
- **Run the servers**: `uv run nox -s dev`
  - The server starts on port 8000 by default. CORS allows `http://localhost:5173` in development.
- **Configuration**: Edit the `.env` if available, otherwise copy from `.env.example`.
- **Testing**: `uv run nox -s tests` (runs in `development` env by default)
- **Linting**: `uv run nox -s fix` and `uv run nox -s lint`

### Frontend (React)
- **Package Manager**: Uses `npm`. All commands should be run from the `frontend/` directory.
- **Environment variables**: Copy `frontend/.env.example` to `.env` and adjust `VITE_API_URL` if needed. Default points to `http://127.0.0.1:8000/`.
- **Development**: `uv run nox -s dev` — Starts both fontend and backend. Starts Vite on port 5173 with HMR.
- **Build**: `npm run build` — production build via React Router.
- **Type checking**: `npm run typecheck` — runs `react-router typegen && tsc`.
- **Linting/formatting**: `uv run nox -s frontend` — runs build, ts compile, and Biome check with auto-fix.

### Full stack (Nox)
Run all checks: `uv run nox`
Available sessions (`uv run nox -l`):
- `lint` — ruff format/check + mypy on backend Python code
- `fix` — ruff format + auto-fix
- `security` — bandit + pip-audit for dependency vulnerabilities
- `tests` — pytest with coverage (env set to `development`)
- `frontend` — npm ci, build, and lint in the frontend directory
- `dev` — runs both backend (`fastapi dev`) and frontend (`npm run dev`) concurrently via `npx concurrently --kill-others`
