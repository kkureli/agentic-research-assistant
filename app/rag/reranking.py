from app.schemas.document import Document
from app.schemas.retrieval import RerankResult
from app.services.llm import generate_structured_output


RERANK_SYSTEM_PROMPT = """
You are a retrieval reranker.

Your task is to evaluate candidate document chunks based on how useful
they are for answering the original user question.

Rules:
- Score every candidate from 0.0 to 1.0.
- Higher scores mean the chunk is more relevant.
- Evaluate relevance against the original user question.
- Prefer chunks that directly contain evidence needed to answer the question.
- Do not give a high score merely because a chunk mentions the same company or topic.
- Consider whether the chunk helps answer all or part of the question.
- Do not answer the user's question.
- Return every chunk ID exactly as provided.
"""


def rerank_documents(
    question: str,
    documents: list[Document],
    top_k: int = 5,
) -> list[Document]:
    candidates = []

    for document in documents:
        candidates.append(
            f"""
Chunk ID: {document.metadata["chunk_id"]}
Text:
{document.text}
"""
        )

    user_prompt = f"""
Original question:
{question}

Candidate chunks:

{"\n\n".join(candidates)}
"""

    result = generate_structured_output(
        system_prompt=RERANK_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        output_type=RerankResult,
    )

    scores_by_id = {item.chunk_id: item.score for item in result.results}

    ranked_documents = sorted(
        documents,
        key=lambda document: scores_by_id.get(
            document.metadata["chunk_id"],
            0.0,
        ),
        reverse=True,
    )

    return ranked_documents[:top_k]


if __name__ == "__main__":
    from app.rag.query_decomposition import decompose_query
    from app.rag.retrieval_utils import deduplicate_documents
    from app.rag.retriever import retrieve_multiple

    question = "Compare the main causes of growth slowdown at Asteria and Nova."

    queries = decompose_query(question)

    documents = retrieve_multiple(
        queries,
        top_k=5,
    )

    documents = deduplicate_documents(documents)

    ranked_documents = rerank_documents(
        question=question,
        documents=documents,
        top_k=5,
    )

    print(f"Original question: {question}")
    print(f"Decomposed queries: {queries}")
    print(f"Candidates: {len(documents)}")
    print("-----")

    for document in ranked_documents:
        print(
            document.metadata["chunk_id"],
            "|",
            document.metadata["company"],
        )
