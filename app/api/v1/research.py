from fastapi import APIRouter, Depends, Request, status

from app.api.auth import require_api_key
from app.api.rate_limit import limiter, research_rate_limit
from app.schemas.api import ErrorResponse
from app.schemas.research import ResearchRequest, ResearchResponse
from app.services.research_service import research

router = APIRouter(tags=["research"])


@router.post(
    "/research",
    response_model=ResearchResponse,
    summary="Run a research question",
    description=(
        "Runs the multi-agent research workflow and returns a grounded answer "
        "with citations and runtime metadata. Requires the X-API-Key header."
    ),
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": ErrorResponse},
        status.HTTP_429_TOO_MANY_REQUESTS: {"model": ErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse},
        status.HTTP_502_BAD_GATEWAY: {"model": ErrorResponse},
        status.HTTP_503_SERVICE_UNAVAILABLE: {"model": ErrorResponse},
        status.HTTP_504_GATEWAY_TIMEOUT: {"model": ErrorResponse},
    },
)
@limiter.limit(research_rate_limit)
def run_research(
    request: Request,
    payload: ResearchRequest,
    _: None = Depends(require_api_key),
) -> ResearchResponse:
    return research(payload.question)
