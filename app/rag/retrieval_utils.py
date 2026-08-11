from app.schemas.document import Document


def deduplicate_documents(
    documents: list[Document],
) -> list[Document]:
    seen_ids = set()
    unique_documents = []

    for document in documents:
        chunk_id = document.metadata["chunk_id"]

        if chunk_id in seen_ids:
            continue

        seen_ids.add(chunk_id)
        unique_documents.append(document)

    return unique_documents
