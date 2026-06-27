from pydantic import BaseModel


class ExamQuestion(BaseModel):
    question: str
    answer: str


class MockExamResponse(BaseModel):
    questions: list[ExamQuestion]