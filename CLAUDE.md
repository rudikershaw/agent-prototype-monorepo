# CLAUDE.md

## Project Overview
This is an AI-powered chat application built as a technical assignment for Owkin. The app features a conversational interface where users can ask questions about biotech data (genes, cancer indications, expression values). The backend delegates to an OpenAI-compatible LLM endpoint (default: local LM Studio) using `pydantic_ai` for agent management and streaming responses.

## Tech Stack
- **Backend**: Python 3.12+, FastAPI (`fastapi[standard]`), `pydantic_ai`, `httpx2`, Pydantic
- **Frontend**: React 19, React Router v7 (SSR), Vite, Tailwind CSS 4, TypeScript, `@assistant-ui/react`
- **Tooling**: `uv` (workspace), `nox` (automation), `ruff`, `mypy`, `bandit`, `pip-audit`, `pytest`, Biome

Use `uv run nox -l` and `uv run noc -s ${SESSION}` over manual commands to the various tools.

## Design Decisions
- **Service-layer separation** — Business logic lives in dedicated service classes (`InferenceService`, `CancerGeneExpressionService`, `ToolService`) rather than controllers, making each concern independently testable.
- **Resource loading via path resolution** — Non-Python assets (prompts, CSV data) are loaded through a shared `resources.py` module that resolves paths relative to the package directory, avoiding fragile hardcoded paths or environment variables for asset discovery.
- **Tool call parsing with regex + AST eval** — The `ToolService` extracts tool calls from LLM output using a pair of compiled regexes and evaluates arguments via `ast.literal_eval` for safety, then dispatches to registered handlers by name. This avoids requiring the LLM to produce structured JSON while remaining deterministic.
- **Strict mypy configuration** — All Python code runs under `strict = true` with `disallow_untyped_defs`, ensuring every public function has explicit type annotations and return types.

## Repository Structure
- `backend/` — FastAPI application
  - `src/api/main.py` — App entry point, router registration, CORS setup
  - `src/api/controller/chat.py` — `/chat` POST endpoint (streaming)
  - `src/api/controller/health.py` — `/` GET health check endpoint
  - `src/api/service/inference.py` — `InferenceService` wrapping a `pydantic_ai.Agent` with an OpenAI-compatible model
  - `src/api/service/expression.py` — `CancerGeneExpressionService` for querying the biotech dataset
  - `src/api/service/tools.py` — `ToolService` for parsing and dispatching tool calls from LLM output
  - `src/api/config/` — `InferenceConfig`, CORS settings, and resource path resolution (`resources.py`)
  - `src/api/resources/` — Non-Python assets: system prompt template and the cancer gene expression CSV
- `frontend/` — React application
  - `app/routes/` — Route definitions: home (chat), assistant (standalone chat page), health status
  - `app/components/assistant-ui/` — Custom Assistant UI components (thread, markdown rendering, reasoning panels, tool fallbacks)
  - `app/components/header/` — Header with logo and navigation
  - `app/components/health/` — Health status display component
  - `app/components/welcome/` — Welcome screen for the chat interface
  - `app/utils/chat-model-adapter.ts` — ChatModelAdapter that serializes messages to the backend `/chat` endpoint
  - `app/config.ts` — API URL configuration (`VITE_API_URL`)
  - `Dockerfile` — Multi-stage build for production deployment
- `technical-test/` — Assignment materials (data CSV, spec document)

## Configuration
The app uses environment variables for runtime configuration. Copy `.env.example` to `.env` in each subdirectory and adjust values as needed:

| Variable | Default | Description |
|---|---|---|
| `INFERENCE_HOST` | `http://localhost:1234/v1` | OpenAI-compatible LLM endpoint URL |
| `INFERENCE_MODEL` | `qwen3.6-35b-a3b-uncensored-genesis-v2-apex-mtp` | Model name for inference |
| `VITE_API_URL` | `http://127.0.0.1:8000/` | Backend API base URL (frontend) |

In CI, the `APP_ENV=development` variable is set by the nox test session to control behavior.

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

### Testing Strategy
Tests live under `backend/tests/` with two files:

- **`test_unit.py`** — Unit tests for service classes (`CancerGeneExpressionService`, `ToolService`). Each test exercises a single method in isolation, mocking the CSV data where needed.
- **`test_default.py`** — Default template test that verifies the health endpoint returns 200 OK.

The project enforces coverage via `[tool.coverage.report].fail_under = 98` and runs with branch coverage enabled (`branch = true`). Tests set `APP_ENV=development` and override `INFERENCE_HOST` to avoid hitting an actual LLM endpoint during CI runs.
