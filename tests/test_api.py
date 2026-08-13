from unittest.mock import patch

from fastapi.testclient import TestClient

from app.core.exceptions import AgentMaxStepsError
from app.schemas.research import ResearchResponse


def test_health(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert "X-Request-ID" in response.headers


def test_ready(client: TestClient) -> None:
    with patch("app.api.v1.health._qdrant_is_reachable", return_value=True):
        response = client.get("/ready")

    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_research_success(client: TestClient) -> None:
    mock_response = ResearchResponse(
        answer="Asteria Cloud Systems grew 17% year over year in Q2 2026 [S1].",
        citations=["S1"],
        tool_calls=1,
        research_llm_calls=2,
        critic_llm_calls=1,
        critic_rounds=1,
    )

    with patch("app.api.v1.research.research", return_value=mock_response):
        response = client.post(
            "/api/v1/research",
            json={
                "question": "What was Asteria Cloud Systems' revenue growth in Q2 2026?"
            },
        )

    assert response.status_code == 200
    assert response.json() == {
        "answer": mock_response.answer,
        "citations": ["S1"],
        "tool_calls": 1,
        "research_llm_calls": 2,
        "critic_llm_calls": 1,
        "critic_rounds": 1,
    }


def test_research_invalid_question(client: TestClient) -> None:
    response = client.post(
        "/api/v1/research",
        json={"question": "   "},
    )

    assert response.status_code == 422
    assert response.json() == {
        "code": "invalid_input",
        "message": "Invalid request.",
    }


def test_research_internal_failure(client: TestClient) -> None:
    with patch(
        "app.api.v1.research.research",
        side_effect=AgentMaxStepsError(),
    ):
        response = client.post(
            "/api/v1/research",
            json={"question": "What was Asteria's revenue growth?"},
        )

    assert response.status_code == 504
    assert response.json() == {
        "code": "agent_max_steps",
        "message": "The research agent exceeded its maximum number of steps.",
    }
    assert "traceback" not in response.text.lower()


def test_request_id_is_returned(client: TestClient) -> None:
    response = client.get(
        "/health",
        headers={"X-Request-ID": "client-request-123"},
    )

    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == "client-request-123"
