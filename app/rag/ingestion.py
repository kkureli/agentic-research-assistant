from pathlib import Path

from app.rag.chunking import chunk_document
from app.rag.embeddings import embed_texts
from app.rag.vector_store import create_collection, upsert_chunks
from app.services.document_loader import load_markdown_directory


def ingest_documents() -> None:
    documents = load_markdown_directory(Path("data"))
    print(f"Loaded {len(documents)} documents")
    chunks = []
    for document in documents:
        chunks.extend(chunk_document(document))
    embeddings = embed_texts([chunk.text for chunk in chunks])
    create_collection()
    upsert_chunks(chunks, embeddings)


if __name__ == "__main__":
    ingest_documents()
