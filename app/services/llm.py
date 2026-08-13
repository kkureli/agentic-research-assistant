from typing import TypeVar

from openai import OpenAI
from pydantic import BaseModel

from app.core.config import settings


client = OpenAI(
    api_key=settings.openai_api_key,
    timeout=settings.openai_timeout_seconds,
    max_retries=settings.openai_max_retries,
)

T = TypeVar("T", bound=BaseModel)


def generate_answer(
    system_prompt: str,
    user_prompt: str,
) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
    )

    return response.choices[0].message.content or ""


def generate_structured_output(
    system_prompt: str,
    user_prompt: str,
    output_type: type[T],
) -> T:
    response = client.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        response_format=output_type,
    )

    parsed = response.choices[0].message.parsed

    if parsed is None:
        raise ValueError("LLM did not return a valid structured output")

    return parsed
