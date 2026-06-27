def build_mcq_prompt(notes: str) -> str:
    return f"""
You are a Smart Study Assistant.

Generate 5 multiple-choice questions from the lecture notes.

Rules:
- Each question must have exactly 4 choices.
- Do not label choices with A), B), C), or D).
- Use correct_answer_index to identify the correct choice.
- correct_answer_index must be 0, 1, 2, or 3.
- Add a short explanation.
- Do not add information that is not in the notes.
- Return ONLY valid JSON.
- Do not include markdown.

The JSON must follow this exact structure:

{{
  "mcqs": [
    {{
      "question": "...",
      "choices": [
        "...",
        "...",
        "...",
        "..."
      ],
      "correct_answer_index": 0,
      "explanation": "..."
    }}
  ]
}}

Lecture notes:
{notes}
"""