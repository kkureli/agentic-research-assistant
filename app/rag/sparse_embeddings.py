from fastembed import SparseTextEmbedding


sparse_model = SparseTextEmbedding(
    model_name="Qdrant/bm25",
)


def embed_sparse_texts(texts: list[str]):
    return list(sparse_model.embed(texts))
