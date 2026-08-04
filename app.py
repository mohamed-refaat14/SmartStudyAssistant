import streamlit as st

from services.document_service import (
    extract_pdf_pages,
    extract_pdf_text,
)
from services.rag_service import (
    answer_document_question,
    build_document_index,
)
from services.study_service import (
    generate_concepts,
    generate_flashcards,
    generate_mcqs,
    generate_mock_exam,
    generate_summary,
)


st.set_page_config(
    page_title="Smart Study Assistant",
    page_icon="📚",
    layout="centered",
)


# ---------------------------------------------------------
# Session state
# ---------------------------------------------------------

if "rag_chunk_records" not in st.session_state:
    st.session_state.rag_chunk_records = []

if "rag_document_name" not in st.session_state:
    st.session_state.rag_document_name = None


# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------

def build_notes_input(
    typed_notes: str,
    pdf_file,
) -> str:
    typed_notes = typed_notes.strip()
    pdf_text = ""

    if pdf_file is not None:
        pdf_text = extract_pdf_text(pdf_file)

    if typed_notes and pdf_text:
        return (
            "--- Typed Notes ---\n\n"
            f"{typed_notes}\n\n"
            "--- Uploaded PDF ---\n\n"
            f"{pdf_text}"
        )

    if typed_notes:
        return typed_notes

    if pdf_text:
        return pdf_text

    raise ValueError(
        "Please paste lecture notes or upload a PDF first."
    )


def display_summary(
    typed_notes: str,
    pdf_file,
) -> None:
    try:
        combined_notes = build_notes_input(
            typed_notes=typed_notes,
            pdf_file=pdf_file,
        )

        with st.spinner("Generating summary..."):
            result = generate_summary(combined_notes)

        st.subheader("Summary")
        st.markdown(result.summary)

    except ValueError as error:
        st.warning(str(error))

    except Exception as error:
        st.error("The summary could not be generated.")
        st.exception(error)


def display_flashcards(
    typed_notes: str,
    pdf_file,
) -> None:
    try:
        combined_notes = build_notes_input(
            typed_notes=typed_notes,
            pdf_file=pdf_file,
        )

        with st.spinner("Generating flashcards..."):
            result = generate_flashcards(combined_notes)

        st.subheader("Flashcards")

        for index, card in enumerate(
            result.flashcards,
            start=1,
        ):
            st.markdown(f"### Flashcard {index}")
            st.write(f"**Question:** {card.question}")
            st.write(f"**Answer:** {card.answer}")
            st.divider()

    except ValueError as error:
        st.warning(str(error))

    except Exception as error:
        st.error("The flashcards could not be generated.")
        st.exception(error)


def display_mcqs(
    typed_notes: str,
    pdf_file,
) -> None:
    try:
        combined_notes = build_notes_input(
            typed_notes=typed_notes,
            pdf_file=pdf_file,
        )

        with st.spinner("Generating MCQs..."):
            result = generate_mcqs(combined_notes)

        st.subheader("MCQs")

        for question_index, mcq in enumerate(
            result.mcqs,
            start=1,
        ):
            st.markdown(f"### Question {question_index}")
            st.write(mcq.question)

            for choice_index, choice in enumerate(
                mcq.choices
            ):
                choice_label = chr(65 + choice_index)

                if choice_index == mcq.correct_answer_index:
                    st.success(
                        f"✅ {choice_label}. {choice}"
                    )
                else:
                    st.write(
                        f"{choice_label}. {choice}"
                    )

            with st.expander("Explanation"):
                st.write(mcq.explanation)

            st.divider()

    except ValueError as error:
        st.warning(str(error))

    except Exception as error:
        st.error("The MCQs could not be generated.")
        st.exception(error)


def display_concepts(
    typed_notes: str,
    pdf_file,
) -> None:
    try:
        combined_notes = build_notes_input(
            typed_notes=typed_notes,
            pdf_file=pdf_file,
        )

        with st.spinner("Extracting concepts..."):
            result = generate_concepts(combined_notes)

        st.subheader("Concepts")

        for index, concept in enumerate(
            result.concepts,
            start=1,
        ):
            st.markdown(
                f"### {index}. {concept.name}"
            )
            st.write(concept.explanation)
            st.divider()

    except ValueError as error:
        st.warning(str(error))

    except Exception as error:
        st.error("The concepts could not be extracted.")
        st.exception(error)


def display_mock_exam(
    typed_notes: str,
    pdf_file,
) -> None:
    try:
        combined_notes = build_notes_input(
            typed_notes=typed_notes,
            pdf_file=pdf_file,
        )

        with st.spinner("Generating mock exam..."):
            result = generate_mock_exam(combined_notes)

        st.subheader("Mock Exam")

        for index, question in enumerate(
            result.questions,
            start=1,
        ):
            st.markdown(f"### Question {index}")
            st.write(question.question)

            with st.expander("Model Answer"):
                st.write(question.answer)

            st.divider()

    except ValueError as error:
        st.warning(str(error))

    except Exception as error:
        st.error("The mock exam could not be generated.")
        st.exception(error)


# ---------------------------------------------------------
# Page title
# ---------------------------------------------------------

st.title("📚 Smart Study Assistant")

st.write(
    "Paste lecture notes, upload a PDF, or use both "
    "to generate study materials."
)


# ---------------------------------------------------------
# Study-material generation
# ---------------------------------------------------------

st.header("Generate Study Materials")

notes = st.text_area(
    "Lecture notes",
    height=300,
    placeholder="Paste your lecture notes here...",
)

uploaded_file = st.file_uploader(
    "Upload lecture PDF",
    type=["pdf"],
    key="study_material_pdf",
)

col1, col2 = st.columns(2)

with col1:
    summary_button = st.button(
        "Generate Summary",
        use_container_width=True,
    )

    flashcards_button = st.button(
        "Generate Flashcards",
        use_container_width=True,
    )

    exam_button = st.button(
        "Generate Mock Exam",
        use_container_width=True,
    )

with col2:
    concepts_button = st.button(
        "Extract Concepts",
        use_container_width=True,
    )

    mcq_button = st.button(
        "Generate MCQs",
        use_container_width=True,
    )


if summary_button:
    display_summary(
        typed_notes=notes,
        pdf_file=uploaded_file,
    )

if concepts_button:
    display_concepts(
        typed_notes=notes,
        pdf_file=uploaded_file,
    )

if flashcards_button:
    display_flashcards(
        typed_notes=notes,
        pdf_file=uploaded_file,
    )

if mcq_button:
    display_mcqs(
        typed_notes=notes,
        pdf_file=uploaded_file,
    )

if exam_button:
    display_mock_exam(
        typed_notes=notes,
        pdf_file=uploaded_file,
    )


# ---------------------------------------------------------
# RAG document question answering
# ---------------------------------------------------------

st.divider()

st.header("Ask Your Document")

st.write(
    "Upload a PDF, index it, and ask questions "
    "based only on its content."
)

rag_pdf = st.file_uploader(
    "Upload a PDF for document questions",
    type=["pdf"],
    key="rag_pdf_uploader",
)

index_button = st.button(
    "Index Document",
    use_container_width=True,
)


if index_button:
    if rag_pdf is None:
        st.warning("Please upload a PDF first.")

    else:
        try:
            with st.spinner(
                "Extracting and indexing document..."
            ):
                pages = extract_pdf_pages(rag_pdf)

                chunk_records = build_document_index(
                    pages=pages,
                    filename=rag_pdf.name,
                    chunk_size=300,
                    overlap=50,
                )

                st.session_state.rag_chunk_records = (
                    chunk_records
                )

                st.session_state.rag_document_name = (
                    rag_pdf.name
                )

            st.success(
                f"Indexed {len(chunk_records)} chunks "
                f"from {rag_pdf.name}."
            )

        except ValueError as error:
            st.warning(str(error))

        except Exception as error:
            st.error(
                "The document could not be indexed."
            )
            st.exception(error)


if st.session_state.rag_chunk_records:
    st.info(
        "Current indexed document: "
        f"{st.session_state.rag_document_name}"
    )

    rag_question = st.text_input(
        "Ask a question about the uploaded document",
        placeholder="For example: What is overfitting?",
    )

    ask_button = st.button(
        "Ask Document",
        use_container_width=True,
    )

    if ask_button:
        try:
            with st.spinner(
                "Retrieving relevant information..."
            ):
                answer, sources = (
                    answer_document_question(
                        question=rag_question,
                        chunk_records=(
                            st.session_state
                            .rag_chunk_records
                        ),
                        top_k=3,
                    )
                )

            st.subheader("Answer")
            st.write(answer)

            if sources:
                with st.expander(
                    "Retrieved Sources"
                ):
                    for source_number, source in enumerate(
                        sources,
                        start=1,
                    ):
                        filename = source.get(
                            "filename",
                            st.session_state
                            .rag_document_name,
                        )

                        page_number = source.get(
                            "page_number",
                            "Unknown",
                        )

                        chunk_number = (
                            source["chunk_index"] + 1
                        )

                        similarity_score = source[
                            "score"
                        ]

                        st.markdown(
                            f"### Source {source_number}"
                        )

                        st.write(
                            f"**File:** {filename}"
                        )

                        st.write(
                            f"**Page:** {page_number}"
                        )

                        st.write(
                            f"**Chunk:** {chunk_number}"
                        )

                        st.write(
                            "**Similarity score:** "
                            f"{similarity_score:.4f}"
                        )

                        st.write(source["text"])
                        st.divider()

            else:
                st.caption(
                    "No source chunks passed the "
                    "minimum similarity threshold."
                )

        except ValueError as error:
            st.warning(str(error))

        except Exception as error:
            st.error(
                "The question could not be answered."
            )
            st.exception(error)
