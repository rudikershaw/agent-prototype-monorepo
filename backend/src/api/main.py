# ruff: disable[E402, I001]
"""Main application module."""

from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

from api.config.cors import configure_cors
from api.controller.chat import router as chat_router
from api.controller.health import router as health_router
# ruff:enable[E402, I001]

app = FastAPI()
configure_cors(app)
app.include_router(health_router)
app.include_router(chat_router)
