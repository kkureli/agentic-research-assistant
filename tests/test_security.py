from unittest.mock import patch

from fastapi.testclient import TestClient
from openai import OpenAIError

from app.core.config import settings
from app.schemas.research import ResearchResponse
from tests.conftest import AUTH_HEADERS


MOCK_RESPONSE = ResearchResponse(
    answer="Asteria Cloud Systems grew 17% year over year in Q2 2026 [S1].",
    citations=["S1"],
    tool_calls=1,
    research_llm_calls=2,
    critic_llm_calls=1,
    critic_rounds=1,
)


def test_missing_api_key_returns_401(client: TestClient) -> None:
    response = client.post(
        "/api/v1/research",
        json={"question": "What was Asteria's revenue growth?"},
    )

    assert response.status_code == 401
    assert response.json() == {
        "code": "unauthorized",
        "message": "Invalid or missing API key.",
    }


def test_invalid_api_key_returns_401(client: TestClient) -> None:
    response = client.post(
        "/api/v1/research",
        headers={"X-API-Key": "wrong-key"},
        json={"question": "What was Asteria's revenue growth?"},
    )

    assert response.status_code == 401
    assert response.json() == {
        "code": "unauthorized",
        "message": "Invalid or missing API key.",
    }


def test_valid_api_key_continues(client: TestClient) -> None:
    with patch("app.api.v1.research.research", return_value=MOCK_RESPONSE):
        response = client.post(
            "/api/v1/research",
            headers=AUTH_HEADERS,
            json={"question": "What was Asteria's revenue growth?"},
        )

    assert response.status_code == 200
    assert response.json()["citations"] == ["S1"]


def test_rate_limit_exceeded_returns_429(client: TestClient, monkeypatch) -> None:
    monkeypatch.setattr(settings, "rate_limit_per_minute", 1)

    with patch("app.api.v1.research.research", return_value=MOCK_RESPONSE):
        first = client.post(
            "/api/v1/research",
            headers=AUTH_HEADERS,
            json={"question": "What was Asteria's revenue growth?"},
        )
        second = client.post(
            "/api/v1/research",
            headers=AUTH_HEADERS,
            json={"question": "What was Asteria's revenue growth?"},
        )

    assert first.status_code == 200
    assert second.status_code == 429
    assert second.json() == {
        "code": "rate_limit_exceeded",
        "message": "Rate limit exceeded. Try again later.",
    }


def test_external_dependency_error_returns_5xx(client: TestClient) -> None:
    with patch(
        "app.api.v1.research.research",
        side_effect=OpenAIError("upstream timeout"),
    ):
        response = client.post(
            "/api/v1/research",
            headers=AUTH_HEADERS,
            json={"question": "What was Asteria's revenue growth?"},
        )

    assert response.status_code == 502
    assert response.json() == {
        "code": "openai_error",
        "message": "The language model service is unavailable.",
    }


def test_request_id_returned_on_auth_failure(client: TestClient) -> None:
    response = client.post(
        "/api/v1/research",
        headers={"X-Request-ID": "fail-auth-1"},
        json={"question": "What was Asteria's revenue growth?"},
    )

    assert response.status_code == 401
    assert response.headers["X-Request-ID"] == "fail-auth-1"


def test_request_id_returned_on_upstream_failure(client: TestClient) -> None:
    with patch(
        "app.api.v1.research.research",
        side_effect=OpenAIError("upstream timeout"),
    ):
        response = client.post(
            "/api/v1/research",
            headers={**AUTH_HEADERS, "X-Request-ID": "fail-upstream-1"},
            json={"question": "What was Asteria's revenue growth?"},
        )

    assert response.status_code == 502
    assert response.headers["X-Request-ID"] == "fail-upstream-1"


def test_health_does_not_require_api_key(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
