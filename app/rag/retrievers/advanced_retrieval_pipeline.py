from app.rag.metadata_filtering import extract_retrieval_filter
from app.rag.query_decomposition import decompose_query
from app.rag.query_rewriting import rewrite_query
from app.rag.reranking import rerank_documents
from app.rag.retrieval_utils import deduplicate_documents
from app.rag.retrievers.hybrid import retrieve_hybrid_filtered
from app.schemas.document import Document


def advanced_retrieve(
    question: str,
    top_k: int = 5,
) -> list[Document]:
    rewritten_query = rewrite_query(question)

    subqueries = decompose_query(rewritten_query)

    documents = []

    for subquery in subqueries:
        retrieval_filter = extract_retrieval_filter(subquery)

        retrieved_documents = retrieve_hybrid_filtered(
            query=subquery,
            retrieval_filter=retrieval_filter,
            top_k=top_k,
        )

        documents.extend(retrieved_documents)

    documents = deduplicate_documents(documents)

    documents = rerank_documents(
        question=question,
        documents=documents,
        top_k=top_k,
    )

    return documents
