import streamlit as st

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

st.write("Paste your lecture notes, then generate study materials.")

notes = st.text_area(
    "Lecture notes",
    height=300,
    placeholder="Paste your lecture notes here...",
)

col1, col2 = st.columns(2)

with col1:
    summary_button = st.button("Generate Summary")
    flashcards_button = st.button("Generate Flashcards")
    exam_button = st.button("Generate Mock Exam")

with col2:
    concepts_button = st.button("Extract Concepts")
    mcq_button = st.button("Generate MCQs")


def display_result(title: str, generator_function) -> None:
    if not notes.strip():
        st.warning("Please paste lecture notes first.")
        return

    try:
        with st.spinner("Generating..."):
            result = generator_function(notes)

        st.subheader(title)
        st.write(result)

    except Exception as e:
        st.error("Something went wrong.")
        st.exception(e)


if summary_button:
    display_result("Summary", generate_summary)

if concepts_button:
    display_result("Concepts", generate_concepts)

if flashcards_button:
    display_result("Flashcards", generate_flashcards)

if mcq_button:
    display_result("MCQs", generate_mcqs)

if exam_button:
    display_result("Mock Exam", generate_mock_exam)