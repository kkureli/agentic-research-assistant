from app.schemas.document import Document


def build_context(documents: list[Document]) -> str:
    parts = []

    for i, document in enumerate(documents, start=1):
        source = document.metadata["source"]
        chunk_index = document.metadata["chunk_index"]
        text = document.text

        parts.append(
            f"[S{i}]\nSource: {source}\nChunk Index: {chunk_index}\nText: {text}"
        )

    return "\n\n".join(parts)
