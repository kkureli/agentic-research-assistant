from fastapi import APIRouter, status

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
        "with citations and runtime metadata."
    ),
    responses={
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": ErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse},
        status.HTTP_502_BAD_GATEWAY: {"model": ErrorResponse},
        status.HTTP_503_SERVICE_UNAVAILABLE: {"model": ErrorResponse},
        status.HTTP_504_GATEWAY_TIMEOUT: {"model": ErrorResponse},
    },
)
def run_research(request: ResearchRequest) -> ResearchResponse:
    return research(request.question)
