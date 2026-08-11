from qdrant_client.models import (
    Fusion,
    FusionQuery,
    Prefetch,
    SparseVector,
)

from app.core.config import settings
from app.rag.embeddings import embed_texts
from app.rag.metadata_filtering import build_qdrant_filter
from app.rag.sparse_embeddings import embed_sparse_texts
from app.rag.vector_store import client
from app.schemas.document import Document
from app.schemas.retrieval import RetrievalFilter


def retrieve_hybrid(
    query: str,
    top_k: int = 5,
) -> list[Document]:
    dense_embedding = embed_texts([query])[0]
    sparse_embedding = embed_sparse_texts([query])[0]

    response = client.query_points(
        collection_name=settings.qdrant_collection,
        prefetch=[
            Prefetch(
                query=dense_embedding,
                using="dense",
                limit=top_k * 2,
            ),
            Prefetch(
                query=SparseVector(
                    indices=sparse_embedding.indices.tolist(),
                    values=sparse_embedding.values.tolist(),
                ),
                using="sparse",
                limit=top_k * 2,
            ),
        ],
        query=FusionQuery(
            fusion=Fusion.RRF,
        ),
        limit=top_k,
        with_payload=True,
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


def retrieve_hybrid_filtered(
    query: str,
    retrieval_filter: RetrievalFilter,
    top_k: int = 5,
) -> list[Document]:
    dense_embedding = embed_texts([query])[0]
    sparse_embedding = embed_sparse_texts([query])[0]

    qdrant_filter = build_qdrant_filter(retrieval_filter)

    response = client.query_points(
        collection_name=settings.qdrant_collection,
        prefetch=[
            Prefetch(
                query=dense_embedding,
                using="dense",
                filter=qdrant_filter,
                limit=top_k * 2,
            ),
            Prefetch(
                query=SparseVector(
                    indices=sparse_embedding.indices.tolist(),
                    values=sparse_embedding.values.tolist(),
                ),
                using="sparse",
                filter=qdrant_filter,
                limit=top_k * 2,
            ),
        ],
        query=FusionQuery(
            fusion=Fusion.RRF,
        ),
        limit=top_k,
        with_payload=True,
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
