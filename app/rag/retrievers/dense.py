from app.core.config import settings
from app.rag.embeddings import embed_texts
from app.rag.metadata_filtering import build_qdrant_filter
from app.rag.vector_store import client
from app.schemas.document import Document
from app.schemas.retrieval import RetrievalFilter


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


def retrieve_filtered(
    query: str,
    retrieval_filter: RetrievalFilter,
    top_k: int = 5,
) -> list[Document]:
    query_embedding = embed_texts([query])[0]

    qdrant_filter = build_qdrant_filter(retrieval_filter)

    response = client.query_points(
        collection_name=settings.qdrant_collection,
        query=query_embedding,
        query_filter=qdrant_filter,
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
