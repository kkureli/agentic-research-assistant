import logging
import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

REQUEST_ID_HEADER = "X-Request-ID"

logger = logging.getLogger(__name__)


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = request.headers.get(REQUEST_ID_HEADER) or str(uuid.uuid4())
        request.state.request_id = request_id

        started_at = time.perf_counter()

        logger.info(
            "Request started request_id=%s method=%s path=%s",
            request_id,
            request.method,
            request.url.path,
        )

        try:
            response = await call_next(request)
        except Exception:
            latency_seconds = time.perf_counter() - started_at
            logger.exception(
                "Request failed request_id=%s method=%s path=%s latency=%.2fs",
                request_id,
                request.method,
                request.url.path,
                latency_seconds,
            )
            raise

        latency_seconds = time.perf_counter() - started_at

        logger.info(
            "Request completed request_id=%s method=%s path=%s status=%s latency=%.2fs",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            latency_seconds,
        )

        response.headers[REQUEST_ID_HEADER] = request_id

        return response
