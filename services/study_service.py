import json
from typing import TypeVar

from pydantic import BaseModel, ValidationError

from models.concept import ConceptResponse
from models.exam import MockExamResponse
from models.flashcard import FlashcardResponse
from models.mcq import MCQResponse
from models.summary import SummaryResponse
from prompts.concept_prompt import build_concept_prompt
from prompts.exam_prompt import build_exam_prompt
from prompts.flashcard_prompt import build_flashcard_prompt
from prompts.mcq_prompt import build_mcq_prompt
from prompts.summary_prompt import build_summary_prompt
from services.llm_service import ask_llm


T = TypeVar("T", bound=BaseModel)


def _validate_notes(notes: str) -> None:
    if not notes.strip():
        raise ValueError("Lecture notes cannot be empty.")


def _generate_structured_from_notes(notes: str, prompt_builder, response_model: type[T]) -> T:
    _validate_notes(notes)

    prompt = prompt_builder(notes)
    response_text = ask_llm(prompt)

    try:
        data = json.loads(response_text)
        result = response_model.model_validate(data)
        return result

    except json.JSONDecodeError:
        raise ValueError("LLM returned invalid JSON")

    except ValidationError:
        raise ValueError(f"LLM returned JSON, but it does not match {response_model.__name__}")


def generate_summary(notes: str) -> SummaryResponse:
    return _generate_structured_from_notes(notes, build_summary_prompt, SummaryResponse)


def generate_concepts(notes: str) -> ConceptResponse:
    return _generate_structured_from_notes(notes, build_concept_prompt, ConceptResponse)


def generate_flashcards(notes: str) -> FlashcardResponse:
    return _generate_structured_from_notes(notes, build_flashcard_prompt, FlashcardResponse)


def generate_mcqs(notes: str) -> MCQResponse:
    return _generate_structured_from_notes(notes, build_mcq_prompt, MCQResponse)


def generate_mock_exam(notes: str) -> MockExamResponse:
    return _generate_structured_from_notes(notes, build_exam_prompt, MockExamResponse)