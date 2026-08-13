import logging
import time
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FuturesTimeoutError

from app.agents.research_agent import run_research_agent
from app.core.config import settings
from app.core.exceptions import AgentMaxStepsError, ResearchTimeoutError
from app.core.request_context import get_request_id
from app.schemas.research import ResearchResponse
from app.utils.citations import extract_citations

logger = logging.getLogger(__name__)


def research(question: str) -> ResearchResponse:
    """Run research with an outer request timeout.

    Limitation: ``future.result(timeout=...)`` stops waiting for the HTTP
    response, but does not cancel the worker thread. The agent may continue
    until dependency-level timeouts, max agent steps, max critic rounds, or
    max tool calls stop the work. True cancellation is not practical on this
    synchronous stack without unsafe thread kills.
    """
    started_at = time.perf_counter()
    logger.info("Research request started")

    try:
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(_run_research, question)

            try:
                response = future.result(timeout=settings.research_timeout_seconds)
            except FuturesTimeoutError as exc:
                logger.warning(
                    "Research failed error_category=timeout latency=%.2fs",
                    time.perf_counter() - started_at,
                )
                raise ResearchTimeoutError() from exc
    except RuntimeError as exc:
        if "exceeded maximum steps" in str(exc):
            logger.warning(
                "Research failed error_category=agent_max_steps latency=%.2fs",
                time.perf_counter() - started_at,
            )
            raise AgentMaxStepsError() from exc

        logger.exception(
            "Research failed error_category=internal_error latency=%.2fs",
            time.perf_counter() - started_at,
        )
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
    result = run_research_agent(
        question,
        max_steps=settings.max_agent_steps,
        max_critic_rounds=settings.max_critic_rounds,
        max_tool_calls=settings.max_tool_calls_per_request,
    )

    citations = extract_citations(result.answer)
    last_critic = result.critic_traces[-1] if result.critic_traces else None
    tool_names = ",".join(trace.tool_name for trace in result.traces) or "-"
    critic_sufficient = (
        "-" if last_critic is None else str(last_critic.sufficient).lower()
    )

    logger.info(
        "Research audit request_id=%s timestamp=%.3f tool_names=%s "
        "tool_call_count=%s research_llm_calls=%s critic_llm_calls=%s "
        "critic_rounds=%s critic_sufficient=%s citations=%s",
        get_request_id() or "-",
        time.time(),
        tool_names,
        len(result.traces),
        result.llm_call_count,
        result.critic_llm_call_count,
        len(result.critic_traces),
        critic_sufficient,
        ",".join(citations) or "-",
    )

    return ResearchResponse(
        answer=result.answer,
        citations=citations,
        tool_calls=len(result.traces),
        research_llm_calls=result.llm_call_count,
        critic_llm_calls=result.critic_llm_call_count,
        critic_rounds=len(result.critic_traces),
    )
