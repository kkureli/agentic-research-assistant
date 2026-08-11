from app.rag.retrievers.advanced_retrieval_pipeline import advanced_retrieve


def search_knowledge_base(
    query: str,
    top_k: int = 5,
) -> str:
    documents = advanced_retrieve(
        question=query,
        top_k=top_k,
    )

    if not documents:
        return "No relevant evidence found."

    results = []

    for index, document in enumerate(documents, start=1):
        source = document.metadata.get("source", "unknown")

        results.append(f"[S{index}]\nSource: {source}\nContent:\n{document.text}")

    return "\n\n".join(results)
