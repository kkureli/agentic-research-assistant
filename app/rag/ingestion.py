from pathlib import Path

from app.rag.chunking import chunk_document
from app.rag.embeddings import embed_texts
from app.rag.sparse_embeddings import embed_sparse_texts
from app.rag.vector_store import recreate_collection, upsert_chunks
from app.services.document_loader import load_markdown_directory


def ingest_documents() -> None:
    documents = load_markdown_directory(Path("data"))

    chunks = []

    for document in documents:
        chunks.extend(chunk_document(document))

    texts = [chunk.text for chunk in chunks]

    dense_embeddings = embed_texts(texts)
    sparse_embeddings = embed_sparse_texts(texts)

    recreate_collection()

    upsert_chunks(
        chunks=chunks,
        dense_embeddings=dense_embeddings,
        sparse_embeddings=sparse_embeddings,
    )


if __name__ == "__main__":
    ingest_documents()
