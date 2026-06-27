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


def validate_notes() -> bool:
    if not notes.strip():
        st.warning("Please paste lecture notes first.")
        return False
    return True


def display_summary() -> None:
    if not validate_notes():
        return

    try:
        with st.spinner("Generating summary..."):
            result = generate_summary(notes)

        st.subheader("Summary")
        st.markdown(result.summary)

    except Exception as e:
        st.error("Something went wrong.")
        st.exception(e)


def display_flashcards() -> None:
    if not validate_notes():
        return

    try:
        with st.spinner("Generating flashcards..."):
            result = generate_flashcards(notes)

        st.subheader("Flashcards")

        for index, card in enumerate(result.flashcards, start=1):
            st.markdown(f"### Flashcard {index}")
            st.write(f"**Question:** {card.question}")
            st.write(f"**Answer:** {card.answer}")
            st.divider()

    except Exception as e:
        st.error("Something went wrong.")
        st.exception(e)


def display_mcqs() -> None:
    if not validate_notes():
        return

    try:
        with st.spinner("Generating MCQs..."):
            result = generate_mcqs(notes)

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

    except Exception as e:
        st.error("Something went wrong.")
        st.exception(e)


def display_concepts() -> None:
    if not validate_notes():
        return

    try:
        with st.spinner("Extracting concepts..."):
            result = generate_concepts(notes)

        st.subheader("Concepts")

        for index, concept in enumerate(result.concepts, start=1):
            st.markdown(f"### {index}. {concept.name}")
            st.write(concept.explanation)
            st.divider()

    except Exception as e:
        st.error("Something went wrong.")
        st.exception(e)


def display_mock_exam() -> None:
    if not validate_notes():
        return

    try:
        with st.spinner("Generating mock exam..."):
            result = generate_mock_exam(notes)

        st.subheader("Mock Exam")

        for index, question in enumerate(result.questions, start=1):
            st.markdown(f"### Question {index}")
            st.write(question.question)

            with st.expander("Model Answer"):
                st.write(question.answer)

            st.divider()

    except Exception as e:
        st.error("Something went wrong.")
        st.exception(e)


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