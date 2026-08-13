import logging
import time
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FuturesTimeoutError

from app.agents.research_agent import run_research_agent
from app.core.config import settings
from app.core.exceptions import AgentMaxStepsError, ResearchTimeoutError
from app.schemas.research import ResearchResponse
from app.utils.citations import extract_citations

logger = logging.getLogger(__name__)


def research(question: str) -> ResearchResponse:
    started_at = time.perf_counter()
    logger.info("Research request started")

    try:
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(_run_research, question)

            try:
                response = future.result(timeout=settings.research_timeout_seconds)
            except FuturesTimeoutError as exc:
                raise ResearchTimeoutError() from exc
    except RuntimeError as exc:
        if "exceeded maximum steps" in str(exc):
            raise AgentMaxStepsError() from exc

        raise

    latency_seconds = time.perf_counter() - started_at

    logger.info(
        "Research request completed latency=%.2fs tool_calls=%s "
        "research_llm_calls=%s critic_llm_calls=%s critic_rounds=%s",
        latency_seconds,
        response.tool_calls,
        response.research_llm_calls,
        response.critic_llm_calls,
        response.critic_rounds,
    )

    return response


def _run_research(question: str) -> ResearchResponse:
    result = run_research_agent(question)

    return ResearchResponse(
        answer=result.answer,
        citations=extract_citations(result.answer),
        tool_calls=len(result.traces),
        research_llm_calls=result.llm_call_count,
        critic_llm_calls=result.critic_llm_call_count,
        critic_rounds=len(result.critic_traces),
    )
