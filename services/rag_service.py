

from prompts.rag_prompt import build_rag_prompt
from services.chunking_service import split_text
from services.embedding_service import embed_text, embed_texts
from services.llm_service import ask_llm as generate_response
from services.retrieval_service import retrieve_top_k

def build_document_index(
    pages: list[dict],
    filename: str,
    chunk_size: int = 300,
    overlap: int = 50,
) -> list[dict]:
    filename = filename.strip()

    if not filename:
        raise ValueError(
            "The document filename cannot be empty."
        )

    if not pages:
        raise ValueError(
            "The document does not contain any pages."
        )

    chunk_records = []

    for page in pages:
        page_number = page["page_number"]
        page_text = page["text"]

        page_chunks = split_text(
            text=page_text,
            chunk_size=chunk_size,
            overlap=overlap,
        )

        for chunk in page_chunks:
            chunk_records.append(
                {
                    "text": chunk,
                    "page_number": page_number,
                    "filename": filename,
                }
            )

    if not chunk_records:
        raise ValueError(
            "The document did not produce any chunks."
        )

    chunk_texts = [
        record["text"]
        for record in chunk_records
    ]

    embeddings = embed_texts(chunk_texts)

    for index, (record, embedding) in enumerate(
        zip(chunk_records, embeddings)
    ):
        record["chunk_index"] = index
        record["embedding"] = embedding

    return chunk_records

def answer_document_question(
    question: str,
    chunk_records: list[dict],
    top_k: int = 3,
    minimum_score: float = 0.25,
) -> tuple[str, list[dict]]:
    question = question.strip()

    if not question:
        raise ValueError("Please enter a question.")

    if not chunk_records:
        raise ValueError("No document index is available.")

    query_embedding = embed_text(question)

    retrieved_chunks = retrieve_top_k(
        query_embedding=query_embedding,
        chunk_records=chunk_records,
        top_k=top_k,
    )

    relevant_chunks = [
        record
        for record in retrieved_chunks
        if record["score"] >= minimum_score
    ]

    if not relevant_chunks:
        return (
            "I could not find enough information in the uploaded document.",
            [],
        )

    context = "\n\n".join(
        (
            f"[Chunk {record['chunk_index'] + 1}]\n"
            f"{record['text']}"
        )
        for record in relevant_chunks
    )

    prompt = build_rag_prompt(
        question=question,
        context=context,
    )

    answer = generate_response(prompt)

    return answer, relevant_chunks