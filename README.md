# Owkin Technical Demonstration — AI Chat Agent

A full-stack chat application that delegates to an OpenAI-compatible LLM endpoint for conversational interactions about biotech data (genes, cancer indications, expression values). Built as a technical assignment for Owkin.

[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-005574?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React 19](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://react.dev/)

---

## Overview

This application provides a conversational interface for interacting with an AI agent. Users can ask questions about genes, cancer indications, and gene expression values from the dataset in `technical-test/owkin_take_home_data.csv`.

**Example queries:**
- "What are the main genes involved in lung cancer?"
- "What is the median value expression of genes involved in breast cancer?"
- "How can you help me?"

## Prerequisites

### uv (Python dependency manager)
This project uses [uv](https://github.com/astral-sh/uv) for dependency management and virtual environment management. Install it following the [official documentation](https://docs.astral.sh/uv/getting-started/installation/). Verify with `uv --version` (0.11+ required).

### Node.js
The frontend uses npm and requires Node.js 20+. Install from [nodejs.org](https://nodejs.org/) or via your package manager.

## Quick Start

```bash
# Clone the repository
git clone git@github.com:rudikershaw/agent-prototype-monorepo.git && cd agent-prototype-monorepo

# Start both servers
cd frontend && npm install && cd ..
uv run nox -s dev
```

This starts:
- **Backend** on `http://localhost:8000` (FastAPI dev server with auto-reload)
- **Frontend** on `http://localhost:5173` (Vite dev server with HMR)

## Project Structure

```
.
├── backend/                    # FastAPI application
│   ├── pyproject.toml          # Python dependencies and tool config
│   ├── src/api/
│   │   ├── main.py             # App entry point, router registration
│   │   ├── controller/         # Route handlers (chat, health)
│   │   ├── service/            # Business logic (inference service)
│   │   └── config/             # Settings (LLM config, CORS)
│   └── tests/                  # Backend tests
├── frontend/                   # React application
│   ├── app/                    # React Router routes and components
│   ├── package.json            # Node dependencies
│   └── Dockerfile              # Multi-stage production build
├── technical-test/             # Assignment materials
│   ├── assigment-overview.md   # Original spec document
│   └── owkin_take_home_data.csv  # Biotech dataset
├── pyproject.toml              # uv workspace config (Python version)
├── noxfile.py                  # Automation sessions (lint, test, build)
└── CLAUDE.md                   # Developer reference
```

## Development Workflow

### Backend (Python / FastAPI)

**Run the development server:**
```bash
uv run nox -s dev
```

The API is available at `http://localhost:8000`. Visit `http://localhost:8000/` for the health check endpoint or `http://localhost:5173` for the frontend.

**Configuration:** The LLM connection settings are in [backend/src/api/config/__init__.py](backend/src/api/config/__init__.py). By default, it connects to a local LM Studio instance at `http://localhost:1234/v1` using model `qwen3.6-35b-a3b-uncensored-genesis-v2-apex-mtp`. Change these values in the file or override via environment variables if you use Pydantic's config support.

**Lint and format:**
```bash
# Lint and format checks
uv run -s lint

# Check + auto-fix
uv run -s fix
```

**Run tests:**
```bash
uv run -s tests
```

### Frontend (React / React Router)

**Environment variables:** Copy `.env.example` to `.env` in the `frontend/` directory if you need to change the API URL:
```bash
cd frontend && cp .env.example .env
# Edit VITE_API_URL if your backend runs on a different address
```

**Run the development server:**
```bash
uv run nox -s dev
```

The app is available at `http://localhost:5173`.

**Build, type check, and lint:**
```bash
uv run nox -s frontend
```

### All-in-one (Nox)

All checks can be run together:
```bash
uv run nox          # Run all default sessions
uv run nox -l       # List available sessions
```

## Docker Deployment

The frontend can be containerized using the provided multi-stage [Dockerfile](frontend/Dockerfile):

```bash
# Build the image
docker build -t owkin-chat-frontend ./frontend/

# Run it (point to your API backend)
docker run -p 3000:3000 \
  -e VITE_API_URL=https://your-api.example.com \
  owkin-chat-frontend
```

The container serves the production-built frontend on port 3000. The `VITE_API_URL` environment variable controls where API calls are sent (set this to your backend's address).

## Architecture

### Request Flow

1. **Frontend** (`@assistant-ui/react`) renders a chat thread.
2. User messages are serialized as plain text by the `ChatModelAdapter` ([frontend/app/utils/chat-model-adapter.ts](frontend/app/utils/chat-model-adapter.ts))
3. The adapter sends a POST to the backend `/chat` endpoint (`http://localhost:8000/chat`) with `{ "messages": "<serialized history>" }`
4. **Backend** (`pydantic_ai.Agent`) streams text chunks back via `AsyncIterable[str]`
5. Each chunk is yielded immediately, creating a streaming response

### CORS Configuration

CORS is configured dynamically based on `APP_ENV`:
- **Development** (`APP_ENV=development`): Allows `http://localhost:5173` and `http://127.0.0.1:5173`
- **Production** (`APP_ENV=production`): Requires `ALLOWED_ORIGINS` environment variable (comma-separated list of allowed origins). Raises an error if not set.

## AI Component Design Decisions

### Why pydantic_ai over raw HTTP calls?
The project uses [`pydantic_ai`](https://github.com/anthropic/pydantic-ai) instead of direct `httpx`/`openai` SDK calls for the agent layer. This provides:
- Built-in streaming support via `Agent.run_stream()` with clean async generators
- Type-safe message handling through Pydantic models
- A simple abstraction over any OpenAI-compatible endpoint without deep SDK coupling

### Why an OpenAI-compatible local model?
The default configuration points to a local LM Studio instance (`http://localhost:1234/v1`). This means the app runs on a standard laptop (Mac or Windows, <= 16 GB RAM) without requiring GPU or cloud API keys. The endpoint follows the OpenAI chat completions API format, so any compatible server works.

### Message serialization
The frontend serializes all messages into a single plain-text string (`"ROLE: content\n\n..."`) before sending to the backend. This keeps the API simple and avoids schema versioning between frontend and backend message types. Tool calls are serialized as `[tool: name(args) => result]` strings.

### Trade-offs
- **No per-message memory**: The flat text format loses structured message roles, making it harder to add system/user/assistant distinctions in the protocol. This is acceptable for a PoC but would need refinement for production.
- **Single model**: Only one LLM is configured at a time. Adding model switching or fallback logic would require config changes.
- **No dataset integration yet**: The agent has a system prompt about being a biotech assistant, but the CSV data functions (`get_targets`, `get_expressions`) from the original spec are not wired in as tools. This is the next step for deeper integration.

## License

MIT
