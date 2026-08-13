import hashlib

from fastapi import Request
from slowapi import Limiter

from app.core.config import settings


def _rate_limit_key(request: Request) -> str:
    api_key = request.headers.get("X-API-Key")
    if api_key:
        digest = hashlib.sha256(api_key.encode("utf-8")).hexdigest()[:16]
        return f"api-key:{digest}"

    if request.client and request.client.host:
        return f"ip:{request.client.host}"

    return "anonymous"


def research_rate_limit() -> str:
    return f"{settings.rate_limit_per_minute}/minute"


limiter = Limiter(key_func=_rate_limit_key, default_limits=[])
