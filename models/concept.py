from pydantic import BaseModel


class Concept(BaseModel):
    name: str
    explanation: str


class ConceptResponse(BaseModel):
    concepts: list[Concept]