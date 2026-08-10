from app.rag.context import build_context
from app.rag.prompts import SYSTEM_PROMPT
from app.rag.retriever import retrieve
from app.services.llm import generate_answer


def answer_question(question: str) -> str:
    chunks = retrieve(question)
    context = build_context(chunks)

    user_prompt = f"""
Context:
{context}

Question:
{question}
"""

    answer = generate_answer(
        SYSTEM_PROMPT,
        user_prompt,
    )

    return answer


questions = [
    "How did Asteria's revenue growth change from Q1 to Q2 2026?",
    "Why can AI bookings grow faster than recognized revenue?",
]
