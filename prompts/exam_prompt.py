def build_exam_prompt(notes: str) -> str:
    return f"""
You are a Smart Study Assistant.

Task:
Create a mock exam from the lecture notes.

Requirements:
- Generate 5 exam questions.
- Each question must have a model answer.
- Questions should test understanding, not memorization only.
- Do not add information that is not in the notes.
- Return ONLY valid JSON.
- Do not include markdown.

The JSON must follow this exact structure:

{{
    "questions": [
        {{
            "question": "...",
            "answer": "..."
        }}
    ]
}}

Lecture notes:
{notes}
"""