def build_concept_prompt(notes: str) -> str:
    return f"""
You are a Smart Study Assistant.

Task:
Extract the most important study concepts from the lecture notes.

Requirements:
- Return only important concepts.
- Use bullet points.
- For each concept, include a short explanation.
- Do not add information that is not in the notes.

Lecture notes:
{notes}
"""