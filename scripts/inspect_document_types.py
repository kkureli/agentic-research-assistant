# scripts/inspect_document_types.py

from app.core import config
from app.rag.vector_store import client


def main():
    document_types = set()
    offset = None

    while True:
        points, offset = client.scroll(
            collection_name=config.settings.qdrant_collection,
            limit=100,
            offset=offset,
            with_payload=True,
            with_vectors=False,
        )

        for point in points:
            payload = point.payload or {}

            document_type = payload.get("document_type")

            if document_type is not None:
                document_types.add(document_type)

        if offset is None:
            break

    print("\nUnique document_type values:")
    print("----------------------------")

    for document_type in sorted(document_types):
        print(document_type)


if __name__ == "__main__":
    main()
