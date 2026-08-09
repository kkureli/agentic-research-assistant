from pathlib import Path

import yaml

from app.rag.chunking import chunk_document
from app.schemas.document import Document


def load_markdown_directory(path: Path) -> list[Document]:
    documents = []

    for file_path in path.glob("*.md"):
        document = load_markdown(file_path)
        documents.append(document)

    return documents


def load_markdown(path: Path) -> Document:
    raw_text = path.read_text(encoding="utf-8")

    metadata = {"source": path.name}

    content = raw_text

    # Markdown dosyasında YAML front matter varsa parse et
    if raw_text.startswith("---"):
        parts = raw_text.split("---", 2)

        if len(parts) == 3:
            metadata_text = parts[1]
            content = parts[2].strip()

            parsed_metadata = yaml.safe_load(metadata_text) or {}

            metadata.update(parsed_metadata)

    return Document(text=content, metadata=metadata)
