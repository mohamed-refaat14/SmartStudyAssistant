from pydantic import BaseModel


class MCQ(BaseModel):
    question: str
    choices: list[str]
    correct_answer_index: int
    explanation: str


class MCQResponse(BaseModel):
    mcqs: list[MCQ]