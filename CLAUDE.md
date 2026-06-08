# CLAUDE.md

## Project Overview
This project is a technical assigment for interviewing with Owkin, a biotech company. You can find the overview of the assignment here - technical-test/assigment-overview.md

It is a full-stack monorepo containing a Python (FastAPI) backend and a React (Vite/React Router) frontend, managed as a `uv` workspace. The backend should delegate to an OpenAPI / LM Studio compatible LLM end-point for having conversations with the Agent.

## Tech Stack
- **Backend**: Python 3.12+, FastAPI, `uv` (workspace), `pytest`, `nox`.
- **Frontend**: React 19, React Router, Vite, Tailwind CSS, Biome, TypeScript.

## Development Workflow

### Backend (Python)
- **Dependency Management**: This is a `uv` workspace. Use `uv sync` to install dependencies for the entire project or specific members.
- **Execution**: Always use `uv run <command>` to ensure you are using the project's virtual environment and tools.
- **Automation (Nox)**: Use `uv run nox` to run all automated checks.
  - Use `uv run nox -l` to list all available automation sessions.
  - Available sessions: `lint`, `security`, `tests`, `frontend`.
- **Testing**: Backend tests are managed via `pytest`.

### Frontend (React)
- **Package Manager**: Uses `npm`.
- **Development**:
  - `npm run dev`: Start the Vite development server.
- **Build & Quality**:
  - `npm run build`: Create a production build.
  - `npm run lint`: Run Biome for linting and formatting.
  - `npm run typecheck`: Run TypeScript type checking.

## Repository Structure
- `backend/`: FastAPI application.
- `frontend/`: React/Vite application.
- `pyproject.toml`: Workspace and project configuration.
- `noxfile.py`: Automation for linting, security, testing, and frontend building.
