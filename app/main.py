import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from openai import OpenAIError
from qdrant_client.http.exceptions import ApiException, ResponseHandlingException
from slowapi.errors import RateLimitExceeded
from tavily.errors import (
    BadRequestError,
    ForbiddenError,
    InvalidAPIKeyError,
    MissingAPIKeyError,
    TimeoutError as TavilyTimeoutError,
    UsageLimitExceededError,
)

from app.api.middleware import RequestContextMiddleware
from app.api.rate_limit import limiter
from app.api.v1.health import router as health_router
from app.api.v1.research import router as research_router
from app.core.config import settings
from app.core.exceptions import AppError
from app.core.logging import setup_logging
from app.schemas.api import ErrorResponse

setup_logging(settings.resolved_log_level)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    if settings.is_production and not settings.api_key:
        raise RuntimeError("API_KEY is required when APP_ENV=production")

    logger.info("Application starting env=%s", settings.app_env)
    yield
    logger.info("Application stopping")


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    debug=settings.debug and not settings.is_production,
    docs_url="/docs" if settings.docs_enabled else None,
    redoc_url="/redoc" if settings.docs_enabled else None,
    openapi_url="/openapi.json" if settings.docs_enabled else None,
    lifespan=lifespan,
)
app.state.limiter = limiter

app.add_middleware(RequestContextMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.resolved_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(research_router, prefix="/api/v1")

QDRANT_ERRORS = (ApiException, ResponseHandlingException)
WEB_SEARCH_ERRORS = (
    BadRequestError,
    ForbiddenError,
    InvalidAPIKeyError,
    MissingAPIKeyError,
    TavilyTimeoutError,
    UsageLimitExceededError,
)


def _error_response(status_code: int, code: str, message: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content=ErrorResponse(code=code, message=message).model_dump(),
    )


@app.exception_handler(AppError)
def handle_app_error(_request: Request, exc: AppError) -> JSONResponse:
    logger.warning("Application error code=%s error_category=%s", exc.code, exc.code)
    return _error_response(exc.status_code, exc.code, exc.message)


@app.exception_handler(RateLimitExceeded)
def handle_rate_limit(_request: Request, _exc: RateLimitExceeded) -> JSONResponse:
    logger.warning("Rate limit exceeded error_category=rate_limit_exceeded")
    return _error_response(
        status.HTTP_429_TOO_MANY_REQUESTS,
        "rate_limit_exceeded",
        "Rate limit exceeded. Try again later.",
    )


@app.exception_handler(RequestValidationError)
def handle_validation_error(
    _request: Request,
    _exc: RequestValidationError,
) -> JSONResponse:
    return _error_response(
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        "invalid_input",
        "Invalid request.",
    )


@app.exception_handler(OpenAIError)
def handle_openai_error(_request: Request, _exc: OpenAIError) -> JSONResponse:
    logger.exception("OpenAI request failed error_category=openai_error")
    return _error_response(
        status.HTTP_502_BAD_GATEWAY,
        "openai_error",
        "The language model service is unavailable.",
    )


def handle_qdrant_error(_request: Request, _exc: Exception) -> JSONResponse:
    logger.exception("Qdrant request failed error_category=vector_store_error")
    return _error_response(
        status.HTTP_503_SERVICE_UNAVAILABLE,
        "vector_store_error",
        "The vector database is unavailable.",
    )


def handle_web_search_error(_request: Request, _exc: Exception) -> JSONResponse:
    logger.exception("Web search request failed error_category=web_search_error")
    return _error_response(
        status.HTTP_502_BAD_GATEWAY,
        "web_search_error",
        "The web search service is unavailable.",
    )


@app.exception_handler(Exception)
def handle_unexpected_error(_request: Request, _exc: Exception) -> JSONResponse:
    logger.exception("Unexpected internal error error_category=internal_error")
    return _error_response(
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        "internal_error",
        "An unexpected error occurred.",
    )


for _qdrant_error in QDRANT_ERRORS:
    app.add_exception_handler(_qdrant_error, handle_qdrant_error)

for _web_search_error in WEB_SEARCH_ERRORS:
    app.add_exception_handler(_web_search_error, handle_web_search_error)
