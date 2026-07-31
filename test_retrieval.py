from services.embedding_service import embed_text, embed_texts
from services.retrieval_service import retrieve_top_k


chunks = [
    "Overfitting occurs when a model learns the training data too closely and performs poorly on unseen data.",
    "SQL joins combine rows from two or more database tables.",
    "Regularization reduces model complexity and may help prevent overfitting.",
    "Classification predicts discrete categories such as spam or not spam.",
]

chunk_embeddings = embed_texts(chunks)

chunk_records = []

for chunk, embedding in zip(chunks, chunk_embeddings):
    chunk_records.append(
        {
            "text": chunk,
            "embedding": embedding,
        }
    )

question = "Why does my model perform badly on new examples?"

query_embedding = embed_text(question)

results = retrieve_top_k(
    query_embedding=query_embedding,
    chunk_records=chunk_records,
    top_k=2,
)

for index, result in enumerate(results, start=1):
    print(f"Result {index}")
    print(f"Score: {result['score']:.4f}")
    print(f"Text: {result['text']}")
    print()