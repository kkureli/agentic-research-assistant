from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.rag.entity_resolution import COMPANY_ALIASES
from app.schemas.document import Document


def get_company_id(company: str | None) -> str | None:
    if company == "Asteria Cloud Systems":
        return COMPANY_ALIASES["asteria"]

    if company == "Nova Mobility":
        return COMPANY_ALIASES["nova"]

    return None


def chunk_document(document: Document) -> list[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    chunks = text_splitter.split_text(document.text)

    company = document.metadata.get("company")
    period = document.metadata.get("period")

    year = None
    quarter = None

    if isinstance(period, str) and period.startswith("Q"):
        quarter_text, year_text = period.split("_")
        quarter = int(quarter_text[1:])
        year = int(year_text)
    elif isinstance(period, int):
        year = period

    return [
        Document(
            text=chunk,
            metadata={
                **document.metadata,
                "company_id": get_company_id(company),
                "year": year,
                "quarter": quarter,
                "chunk_index": i,
                "chunk_id": f"{document.metadata['source']}:{i}",
            },
        )
        for i, chunk in enumerate(chunks)
    ]
