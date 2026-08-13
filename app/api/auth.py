import secrets

from fastapi import Header

from app.core.config import settings
from app.core.exceptions import UnauthorizedError


def require_api_key(
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
) -> None:
    if not settings.auth_required:
        return

    expected = settings.api_key or ""
    provided = x_api_key or ""

    if not expected or not secrets.compare_digest(provided, expected):
        raise UnauthorizedError()
