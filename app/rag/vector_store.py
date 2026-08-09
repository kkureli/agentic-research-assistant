from uuid import NAMESPACE_URL, uuid5

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from app.core.config import settings
from app.schemas.document import Document

client = QdrantClient(url=settings.qdrant_url)


def create_collection() -> None:
    if client.collection_exists(settings.qdrant_collection):
        print(f"Collection {settings.qdrant_collection} already exists")
        return
    client.create_collection(
        collection_name=settings.qdrant_collection,
        vectors_config=VectorParams(
            size=1536,
            distance=Distance.COSINE,
        ),
    )


def upsert_chunks(
    chunks: list[Document],
    embeddings: list[list[float]],
) -> None:
    points = [
        PointStruct(
            id=build_point_id(chunk),
            vector=embedding,
            payload={
                "text": chunk.text,
                **chunk.metadata,
            },
        )
        for chunk, embedding in zip(chunks, embeddings)
    ]

    client.upsert(
        collection_name=settings.qdrant_collection,
        points=points,
    )

    print(f"Upserted {len(chunks)} chunks")


def build_point_id(chunk: Document) -> str:
    source = chunk.metadata["source"]
    chunk_index = chunk.metadata["chunk_index"]

    key = f"{source}:{chunk_index}"

    return str(uuid5(NAMESPACE_URL, key))
