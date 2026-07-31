import numpy as np


def cosine_similarity(
    vec1: list[float],
    vec2: list[float],
) -> float:
    a = np.array(vec1, dtype=float)
    b = np.array(vec2, dtype=float)

    denominator = np.linalg.norm(a) * np.linalg.norm(b)

    if denominator == 0:
        return 0.0

    return float(np.dot(a, b) / denominator)


def retrieve_top_k(
    query_embedding: list[float],
    chunk_records: list[dict],
    top_k: int = 3,
) -> list[dict]:
    if top_k <= 0:
        raise ValueError("top_k must be greater than zero.")

    if not chunk_records:
        return []

    scored_records = []

    for record in chunk_records:
        score = cosine_similarity(
            query_embedding,
            record["embedding"],
        )

        scored_record = record.copy()
        scored_record["score"] = score
        scored_records.append(scored_record)

    scored_records.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return scored_records[:top_k]