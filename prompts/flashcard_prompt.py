def build_flashcard_prompt(notes: str) -> str:
    return f"""
You are a Smart Study Assistant.

Task:
Generate study flashcards from the lecture notes.

Requirements:
- Use question and answer format.
- Focus on important concepts only.
- Keep answers short and clear.
- Do not add information that is not in the notes.

Format:
Q: ...
A: ...

Lecture notes:
{notes}
"""