import streamlit as st

from services.document_service import extract_pdf_text
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


if "rag_chunk_records" not in st.session_state:
    st.session_state.rag_chunk_records = []

if "rag_document_name" not in st.session_state:
    st.session_state.rag_document_name = None


st.title("Smart Study Assistant")

st.write(
    "Paste lecture notes, upload a PDF, or use both to generate "
    "study materials."
)


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


col1, col2 = st.columns(2)

with col1:
    summary_button = st.button("Generate Summary")
    flashcards_button = st.button("Generate Flashcards")
    exam_button = st.button("Generate Mock Exam")

with col2:
    concepts_button = st.button("Extract Concepts")
    mcq_button = st.button("Generate MCQs")


def display_summary() -> None:
    try:
        combined_notes = build_notes_input(
            notes,
            uploaded_file,
        )

        with st.spinner("Generating summary..."):
            result = generate_summary(combined_notes)

        st.subheader("Summary")
        st.markdown(result.summary)

    except ValueError as error:
        st.warning(str(error))

    except Exception as error:
        st.error("Something went wrong.")
        st.exception(error)


def display_flashcards() -> None:
    try:
        combined_notes = build_notes_input(
            notes,
            uploaded_file,
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
        st.error("Something went wrong.")
        st.exception(error)


def display_mcqs() -> None:
    try:
        combined_notes = build_notes_input(
            notes,
            uploaded_file,
        )

        with st.spinner("Generating MCQs..."):
            result = generate_mcqs(combined_notes)

        st.subheader("MCQs")

        for index, mcq in enumerate(
            result.mcqs,
            start=1,
        ):
            st.markdown(f"### Question {index}")
            st.write(mcq.question)

            for choice_index, choice in enumerate(
                mcq.choices
            ):
                if choice_index == mcq.correct_answer_index:
                    st.success(f"✅ {choice}")
                else:
                    st.write(choice)

            with st.expander("Explanation"):
                st.write(mcq.explanation)

            st.divider()

    except ValueError as error:
        st.warning(str(error))

    except Exception as error:
        st.error("Something went wrong.")
        st.exception(error)


def display_concepts() -> None:
    try:
        combined_notes = build_notes_input(
            notes,
            uploaded_file,
        )

        with st.spinner("Extracting concepts..."):
            result = generate_concepts(combined_notes)

        st.subheader("Concepts")

        for index, concept in enumerate(
            result.concepts,
            start=1,
        ):
            st.markdown(f"### {index}. {concept.name}")
            st.write(concept.explanation)
            st.divider()

    except ValueError as error:
        st.warning(str(error))

    except Exception as error:
        st.error("Something went wrong.")
        st.exception(error)


def display_mock_exam() -> None:
    try:
        combined_notes = build_notes_input(
            notes,
            uploaded_file,
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
        st.error("Something went wrong.")
        st.exception(error)


if summary_button:
    display_summary()

if concepts_button:
    display_concepts()

if flashcards_button:
    display_flashcards()

if mcq_button:
    display_mcqs()

if exam_button:
    display_mock_exam()


st.divider()

st.header("Ask Your Document")

st.write(
    "Upload a PDF, index it, then ask questions based only "
    "on its content."
)

rag_pdf = st.file_uploader(
    "Upload a PDF for document questions",
    type=["pdf"],
    key="rag_pdf_uploader",
)

index_button = st.button("Index Document")

if index_button:
    if rag_pdf is None:
        st.warning("Please upload a PDF first.")

    else:
        try:
            with st.spinner(
                "Extracting and indexing document..."
            ):
                document_text = extract_pdf_text(rag_pdf)

                chunk_records = build_document_index(
                    document_text=document_text,
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

    ask_button = st.button("Ask Document")

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

            with st.expander("Retrieved Sources"):
                for index, source in enumerate(
                    sources,
                    start=1,
                ):
                    st.markdown(
                        f"### Source {index} — "
                        f"Chunk "
                        f"{source['chunk_index'] + 1}"
                    )

                    st.write(
                        "Similarity score: "
                        f"{source['score']:.4f}"
                    )

                    st.write(source["text"])
                    st.divider()

        except ValueError as error:
            st.warning(str(error))

        except Exception as error:
            st.error(
                "The question could not be answered."
            )
            st.exception(error)