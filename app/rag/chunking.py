from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.schemas.document import Document


def chunk_document(document: Document) -> list[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    chunks = text_splitter.split_text(document.text)
    return [
        Document(
            text=chunk,
            metadata={**document.metadata, "chunk_index": i},
        )
        for i, chunk in enumerate(chunks)
    ]
