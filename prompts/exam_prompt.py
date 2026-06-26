def build_exam_prompt(notes: str) -> str:
    return f"""
You are a Smart Study Assistant.

Task:
Create a short mock exam from the lecture notes.

Requirements:
- Include 3 short-answer questions.
- Include 3 multiple-choice questions.
- Include 2 true/false questions.
- Add an answer key at the end.
- Do not add information that is not in the notes.

Lecture notes:
{notes}
"""