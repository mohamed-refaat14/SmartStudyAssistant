from prompts.concept_prompt import build_concept_prompt
from prompts.exam_prompt import build_exam_prompt
from prompts.flashcard_prompt import build_flashcard_prompt
from prompts.mcq_prompt import build_mcq_prompt
from prompts.summary_prompt import build_summary_prompt
from services.llm_service import ask_llm


def _validate_notes(notes: str) -> None:
    if not notes.strip():
        raise ValueError("Lecture notes cannot be empty.")


def _generate_from_notes(notes: str, prompt_builder) -> str:
    _validate_notes(notes)

    prompt = prompt_builder(notes)
    result = ask_llm(prompt)

    return result


def generate_summary(notes: str) -> str:
    return _generate_from_notes(notes, build_summary_prompt)


def generate_concepts(notes: str) -> str:
    return _generate_from_notes(notes, build_concept_prompt)


def generate_flashcards(notes: str) -> str:
    return _generate_from_notes(notes, build_flashcard_prompt)


def generate_mcqs(notes: str) -> str:
    return _generate_from_notes(notes, build_mcq_prompt)


def generate_mock_exam(notes: str) -> str:
    return _generate_from_notes(notes, build_exam_prompt)