from uuid import NAMESPACE_URL, uuid5

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    SparseVector,
    SparseVectorParams,
    VectorParams,
)

from app.core.config import settings
from app.schemas.document import Document

client = QdrantClient(url=settings.qdrant_url)


def create_collection() -> None:
    if client.collection_exists(settings.qdrant_collection):
        print(f"Collection {settings.qdrant_collection} already exists")
        return

    client.create_collection(
        collection_name=settings.qdrant_collection,
        vectors_config={
            "dense": VectorParams(
                size=1536,
                distance=Distance.COSINE,
            ),
        },
        sparse_vectors_config={
            "sparse": SparseVectorParams(),
        },
    )


def upsert_chunks(
    chunks: list[Document],
    dense_embeddings: list[list[float]],
    sparse_embeddings,
) -> None:
    points = []

    for chunk, dense_embedding, sparse_embedding in zip(
        chunks,
        dense_embeddings,
        sparse_embeddings,
    ):
        point = PointStruct(
            id=build_point_id(chunk),
            vector={
                "dense": dense_embedding,
                "sparse": SparseVector(
                    indices=sparse_embedding.indices.tolist(),
                    values=sparse_embedding.values.tolist(),
                ),
            },
            payload={
                "text": chunk.text,
                **chunk.metadata,
            },
        )

        points.append(point)

    client.upsert(
        collection_name=settings.qdrant_collection,
        points=points,
        wait=True,
    )

    print(f"Upserted {len(points)} chunks")


def build_point_id(chunk: Document) -> str:
    chunk_id = chunk.metadata["chunk_id"]

    return str(uuid5(NAMESPACE_URL, chunk_id))


def recreate_collection() -> None:
    if client.collection_exists(settings.qdrant_collection):
        client.delete_collection(
            collection_name=settings.qdrant_collection,
        )

    create_collection()
