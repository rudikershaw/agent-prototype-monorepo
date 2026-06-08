<!-- logo / banner placeholder -->

<div align="center">

# Python Project Template

**uv, nox, ruff, mypy, bandit, audit, and pytest.**

[![Version 0.1.0](https://img.shields.io/badge/version-0.1.0-orange?style=for-the-badge)](https://github.com/)
[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![MIT License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)](LICENSE)

</div>

---

Project template for a simple project setup using uv, nox, ruff, mypy, bandit, audit, and pytest. To use, simply fork the project and crack on.

## Prerequisites

### uv

This project uses [uv](https://github.com/astral-sh/uv) for dependency management, virtual environment management, and task running. To install uv, see the [official installation documentation](https://docs.astral.sh/uv/getting-started/installation/).

The project was initialised with uv 0.11.6. You can verify that you have 0.11 or later using `uv --version`.

While working on the project we recommend you use `uv run` to run any project relevant commands, to maintain a consist python version and environment.

## Getting Started

1. Clone the repository.
2. Install dependencies (including dev dependencies):
   ```bash
   uv sync
   ```
3. Run the full `nox` session.
   ```bash
   uv nox run
   ```

## Development Workflow

This project uses [Nox](https://nox.thea.codes/) for task running. All development tasks (linting, formatting, testing) are defined as Nox sessions. While you work on this project, we recommend you use `uv run nox` to run any linting or checks that you need. For specific tasks, please review the `noxfile.py` or use `uv run nox -l` in your terminal.