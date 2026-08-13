import math


def calculate_ndcg(
    relevant_sources: set[str],
    retrieved_sources: list[str],
) -> float:
    dcg = 0.0

    for rank, source in enumerate(retrieved_sources, start=1):
        relevance = 1 if source in relevant_sources else 0

        dcg += relevance / math.log2(rank + 1)

    ideal_relevant_count = min(
        len(relevant_sources),
        len(retrieved_sources),
    )

    idcg = 0.0

    for rank in range(1, ideal_relevant_count + 1):
        idcg += 1 / math.log2(rank + 1)

    if idcg == 0:
        return 0.0

    return dcg / idcg
