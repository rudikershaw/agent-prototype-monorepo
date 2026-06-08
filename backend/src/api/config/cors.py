"""CORS configuration module."""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def configure_cors(app: FastAPI) -> None:
    """Configure CORS middleware for the FastAPI application."""
    app_env = os.getenv("APP_ENV", "production")
    allowed_origins_raw = os.getenv("ALLOWED_ORIGINS")
    dev_origins = ["http://localhost:5173", "http://127.0.0.1:5173"]

    if app_env.lower() == "production":
        if not allowed_origins_raw:
            raise RuntimeError(
                "SECURITY ERROR: 'ALLOWED_ORIGINS' must be set when running in production (APP_ENV=production). "
                "To allow local development origins, set 'APP_ENV=development' or provide 'ALLOWED_ORIGINS'."
            )
        origins = allowed_origins_raw.split(",")
    else:
        origins = allowed_origins_raw.split(",") if allowed_origins_raw else dev_origins

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
