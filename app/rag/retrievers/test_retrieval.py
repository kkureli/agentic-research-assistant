from app.rag.retrievers.advanced_retrieval_pipeline import advanced_retrieve

if __name__ == "__main__":
    question = "Compare the main causes of growth slowdown at Asteria and Nova."

    documents = advanced_retrieve(question)

    for document in documents:
        print(
            document.metadata["chunk_id"],
            "|",
            document.metadata["company"],
        )
