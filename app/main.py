import logging

from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import setup_logging


setup_logging()

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    debug=settings.debug,
)


@app.on_event("startup")
def startup():
    logger.info("Application starting")


@app.get("/health")
def health():
    logger.info("Health check requested")

    return {
        "status": "ok",
        "environment": settings.app_env,
    }
