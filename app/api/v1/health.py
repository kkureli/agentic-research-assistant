import logging

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.schemas.api import HealthResponse, ReadyResponse

logger = logging.getLogger(__name__)

router = APIRouter(tags=["health"])


def _required_settings_available() -> bool:
    return bool(
        settings.openai_api_key
        and settings.tavily_api_key
        and settings.qdrant_url
    )


def _qdrant_is_reachable() -> bool:
    try:
        from app.rag.vector_store import client

        client.get_collections()
        return True
    except Exception:
        logger.warning("Qdrant readiness check failed", exc_info=True)
        return False


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Liveness check",
    description="Returns whether the API process is running.",
)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get(
    "/ready",
    response_model=ReadyResponse,
    summary="Readiness check",
    description="Checks required configuration and Qdrant connectivity.",
    responses={
        status.HTTP_503_SERVICE_UNAVAILABLE: {"model": ReadyResponse},
    },
)
def ready():
    if not _required_settings_available():
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=ReadyResponse(
                status="unavailable",
                reason="missing_configuration",
            ).model_dump(),
        )

    if not _qdrant_is_reachable():
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=ReadyResponse(
                status="unavailable",
                reason="qdrant_unreachable",
            ).model_dump(),
        )

    return ReadyResponse(status="ready")
