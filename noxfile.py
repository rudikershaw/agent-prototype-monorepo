"""Nox sessions for testing, linting, and formatting."""

from nox import Session, options
from nox_uv import session

options.default_venv_backend = "uv"
options.reuse_existing_virtualenvs = True
options.sessions = ["lint", "security", "tests", "frontend"]


@session(uv_no_install_project=True, uv_quiet=True, uv_groups=["lint", "dev"])
def lint(session: Session) -> None:
    """Run linters."""
    session.chdir("backend")
    session.run("ruff", "format", "src", "tests", "../noxfile.py")
    session.run("ruff", "check", "src", "tests", "../noxfile.py")
    session.run("mypy", "src", "../noxfile.py")


@session(uv_no_install_project=True, uv_quiet=True, uv_groups=["lint"])
def fix(session: Session) -> None:
    """Format code with ruff."""
    session.chdir("backend")
    session.run("ruff", "format", "src", "tests", "../noxfile.py")
    session.run("ruff", "check", "--fix", "src", "tests", "../noxfile.py")


@session(uv_no_install_project=True, uv_quiet=True, uv_groups=["lint"])
def security(session: Session) -> None:
    """Audit dependencies for security vulnerabilities."""
    session.chdir("backend")
    session.run("bandit", "-r", "src")
    session.run("uv", "audit", external=True)


@session(uv_quiet=True, uv_groups=["test"])
def tests(session: Session) -> None:
    """Run tests with pytest and check coverage."""
    session.chdir("backend")
    session.env["APP_ENV"] = "development"
    session.run(
        "pytest",
        "tests",
        "--doctest-modules",
    )


@session(venv_backend="none")
def frontend(session: Session) -> None:
    """Build the frontend."""
    session.chdir("frontend")
    session.run("npm", "ci", external=True)
    session.run("npm", "run", "build", external=True)
    session.run("npm", "run", "lint", external=True)


@session(venv_backend="none")
def dev(session: Session) -> None:
    """Run backend and frontend concurrently for integration testing."""
    session.run(
        "bash",
        "-c",
        "npx concurrently --kill-others 'cd backend && \
            APP_ENV=development uv run fastapi dev' 'cd frontend && npm run dev'",
        external=True,
    )
