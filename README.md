# Owkin Technical Demonstration — AI Chat Agent

A chat application that delegates to pydantic AI selected LLM endpoint for conversational interactions about biotech data (genes, cancer indications, expression values). 

[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-005574?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React 19](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://react.dev/)

---

## Overview

The solution is provides relevant answers to the following queries:

* How can you help me?
* What are the main genes involved in lung cancer?
* What is the median value expression of genes involved in breast cancer?
* What is the median value expression of genes involved in esophageal cancer?

Each were tested and confirmed using a local model (a quantised fine tune of Qwen3.6 27B), and Gemini Flash 2.5.

## Prerequisites

### uv (Python dependency manager)
This project uses [uv](https://github.com/astral-sh/uv) for dependency management and virtual environment management. Install it using the [official documentation](https://docs.astral.sh/uv/getting-started/installation/). Verify with `uv --version` (0.11+ required).

### Node.js
The frontend uses npm and requires Node.js 20+. Install from [nodejs.org](https://nodejs.org/) or via your package manager.

## Quick Start

The solution can be run and tested immediately using a free Google API key and Gemini Flash 2.5. I will supply an API key over email when submitting the task.

```bash
# Clone the repository
git clone git@github.com:rudikershaw/agent-prototype-monorepo.git && cd agent-prototype-monorepo

# Full build, lint, tests, etc.
uv run nox

# Copy the backend .env file and then manually edit to include your provider details.
cp backend/.env.example backend/.env 

# Start both servers
uv run nox -s dev
```

This starts:
- **Backend** on `http://localhost:8000` (FastAPI dev server with auto-reload)
- **Frontend** on `http://localhost:5173` (Vite dev server with HMR)

To configure use for your own model or provider
```bash
# Copy the backend .env file and then manually edit to include your provider details.
cp backend/.env.example backend/.env 
```

## Project Structure

The project was assembled using a variety of pre-made templates. The frontend uses the ReactRouterv7 default templates. The backend uses FastAPI's default new project template. The python project that includes the FastAPI app is my own template including a variety of additional linting, testing, and typechecking steps plus task running using `nox`. The agent chat interface is a default that can be initialised with `assistant-ui`, which pulls in a variety of template components into the project. These components were then all wrapped in a python mono-repo format so it could be handed over in one piece. The project directory structure can be seen below.

```
.
├── backend/                    # FastAPI application
│   ├── pyproject.toml          # Python dependencies and tool config
│   ├── src/api/
│   │   ├── main.py             # App entry point, router registration
│   │   ├── controller/         # Route handlers (chat, health)
│   │   ├── service/            # Business logic (inference service, etc)
│   │   └── config/             # Settings utilities (LLM config, CORS)
│   └── tests/                  # Backend tests
├── frontend/                   # React application
│   ├── app/                    # React Router routes and components
│   ├── package.json            # Node dependencies
│   └── Dockerfile              # Frontend docker file
├── pyproject.toml              # uv workspace config (Python version)
├── noxfile.py                  # Automation sessions (lint, test, build)
└── CLAUDE.md                   # Claude Code developer reference
```

## Technical Decisions

### Language model API interaction on the backend.

Assistant UI provides a way of directly connecting to providers through the frontend. I chose to override this functionality and added an adapter to route chat queries to the backend. This keeps API keys, tool calls, and any additional information exposed by tool calls server side. This reduces attack surface and gives us the flexibility to apply guardrails and similar server-side. This also means that the system prompt cannot be exposed (except through LLM jail-breaking).

The backend streams chat to and from the user interface. Tool calls pause streaming while the backend server collects a full tool call, and then resumes streaming when results are available.

Some features not implemented;
* Server side session message tracking.
* Server side guard rails.
* Multi-media processing (images, file uploads, video, etc).

### Further changes.

Below are some features I would have liked to included in the time but were not prioritised;

* Full docker deployments for both frontend and backend with the appropriate ports exposed, effectively ready for production.
* Some linting errors have been suppressed which I would have liked to fix.
* No converstation history in the user interface. Previous conversations are forgotten.
* I would have liked to add additional tools. The two tool calls in the specification have been implemented but there are ways of wording questions that require the model to call tools many many times, when a simple varient of the tool could have provided details in one go.
* A gold-standard data set for important user questions, attack vectors, breaking cases, etc.
* Live trajectory analysis for agent conversations and on-going evaluation.
* Integration testing to evaluate basic agent capabilities remain intact across changes to prompts and services.

### Development Workflow

The project contains a CLAUDE.md file with salient details to allow Claude Code agents to easily explore the project.

The project uses `uv` for running python interpreters, managing virtual environments, and running tools. `nox` is used for task running. The nox sessions encompass all development workflow tasks you might need with a `uv run nox` default command that runs all the important builds, checks, tests, security auditing, etc in order. When you need to run commands, you can use `uv run nox -l` to view all available sessions that can be run. Chaining tasks together has been used to make sure the application can be run, built, and developed with the smallest mental burden for development.

The full stack can be run locally using `uv run nox -s dev`.

### Docker Deployment

A dockerfile is provided for the ReactRouterv77 template React app - [Dockerfile](frontend/Dockerfile):

```bash
# Build the image
docker build -t owkin-chat-frontend ./frontend/

# Run it (point to your API backend)
docker run -p 3000:3000 \
  -e VITE_API_URL=https://your-api.example.com \
  owkin-chat-frontend
```

There is no corresponding Dockerfile for the backend at this time.
