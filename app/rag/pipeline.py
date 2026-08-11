from app.rag.context import build_context
from app.rag.prompts import SYSTEM_PROMPT
from app.rag.retrievers.advanced_retrieval_pipeline import advanced_retrieve
from app.services.llm import generate_answer


def answer_question(question: str) -> str:
    chunks = advanced_retrieve(question)

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


if __name__ == "__main__":
    question = "Compare the main causes of growth slowdown at Asteria and Nova."

    answer = answer_question(question)

    print(f"Question: {question}\n")
    print(f"Answer:\n{answer}")
