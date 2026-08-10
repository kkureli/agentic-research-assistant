from qdrant_client import QdrantClient

from app.core.config import settings
from app.rag.embeddings import embed_texts
from app.schemas.document import Document

client = QdrantClient(url=settings.qdrant_url)


def retrieve(query: str, top_k: int = 5) -> list[Document]:
    embeddings = embed_texts([query])

    response = client.query_points(
        collection_name=settings.qdrant_collection,
        query=embeddings[0],
        limit=top_k,
    )

    return [
        Document(
            text=item.payload["text"],
            metadata={
                key: value for key, value in item.payload.items() if key != "text"
            },
        )
        for item in response.points
    ]
