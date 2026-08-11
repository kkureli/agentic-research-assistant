from app.core.config import settings
from app.rag.embeddings import embed_texts
from app.rag.vector_store import client
from app.schemas.document import Document


def retrieve_multiple(
    queries: list[str],
    top_k: int = 5,
) -> list[Document]:
    embeddings = embed_texts(queries)
    results = []

    for embedding in embeddings:
        response = client.query_points(
            collection_name=settings.qdrant_collection,
            query=embedding,
            limit=top_k,
        )

        documents = [
            Document(
                text=item.payload["text"],
                metadata={
                    key: value for key, value in item.payload.items() if key != "text"
                },
            )
            for item in response.points
        ]

        results.extend(documents)

    return results
