import streamlit as st

from services.document_service import extract_pdf_text
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

st.title("Smart Study Assistant")

st.write(
    "Paste your lecture notes, upload a PDF, or use both to generate "
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
)


def build_notes_input(typed_notes, pdf_file) -> str:
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
        combined_notes = build_notes_input(notes, uploaded_file)

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
        combined_notes = build_notes_input(notes, uploaded_file)

        with st.spinner("Generating flashcards..."):
            result = generate_flashcards(combined_notes)

        st.subheader("Flashcards")

        for index, card in enumerate(result.flashcards, start=1):
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
        combined_notes = build_notes_input(notes, uploaded_file)

        with st.spinner("Generating MCQs..."):
            result = generate_mcqs(combined_notes)

        st.subheader("MCQs")

        for index, mcq in enumerate(result.mcqs, start=1):
            st.markdown(f"### Question {index}")
            st.write(mcq.question)

            for choice_index, choice in enumerate(mcq.choices):
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
        combined_notes = build_notes_input(notes, uploaded_file)

        with st.spinner("Extracting concepts..."):
            result = generate_concepts(combined_notes)

        st.subheader("Concepts")

        for index, concept in enumerate(result.concepts, start=1):
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
        combined_notes = build_notes_input(notes, uploaded_file)

        with st.spinner("Generating mock exam..."):
            result = generate_mock_exam(combined_notes)

        st.subheader("Mock Exam")

        for index, question in enumerate(result.questions, start=1):
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