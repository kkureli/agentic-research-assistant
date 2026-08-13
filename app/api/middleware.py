import logging
import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.request_context import request_id_var

REQUEST_ID_HEADER = "X-Request-ID"

logger = logging.getLogger(__name__)


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = request.headers.get(REQUEST_ID_HEADER) or str(uuid.uuid4())
        request.state.request_id = request_id
        token = request_id_var.set(request_id)
        started_at = time.perf_counter()

        try:
            logger.info(
                "Request started method=%s path=%s",
                request.method,
                request.url.path,
            )

            try:
                response = await call_next(request)
            except Exception:
                latency_seconds = time.perf_counter() - started_at
                logger.exception(
                    "Request failed method=%s path=%s latency=%.2fs error_category=unhandled",
                    request.method,
                    request.url.path,
                    latency_seconds,
                )
                raise

            latency_seconds = time.perf_counter() - started_at
            error_category = _error_category(response.status_code)

            logger.info(
                "Request completed method=%s path=%s status=%s latency=%.2fs error_category=%s",
                request.method,
                request.url.path,
                response.status_code,
                latency_seconds,
                error_category,
            )

            response.headers[REQUEST_ID_HEADER] = request_id
            return response
        finally:
            request_id_var.reset(token)


def _error_category(status_code: int) -> str:
    if status_code < 400:
        return "-"
    if status_code == 401:
        return "unauthorized"
    if status_code == 422:
        return "invalid_input"
    if status_code == 429:
        return "rate_limit_exceeded"
    if status_code == 502:
        return "upstream_error"
    if status_code == 503:
        return "dependency_unavailable"
    if status_code == 504:
        return "timeout"
    if status_code >= 500:
        return "internal_error"
    return "client_error"
