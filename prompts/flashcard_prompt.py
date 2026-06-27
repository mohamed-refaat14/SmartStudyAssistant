def build_flashcard_prompt(notes: str) -> str:
    return f"""
You are a study assistant.

Create flashcards from the notes below.

Return ONLY valid JSON.
Do not include markdown.
Do not include explanations.

The JSON must follow this exact structure:

{{
  "flashcards": [
    {{
      "question": "...",
      "answer": "..."
    }}
  ]
}}

Notes:
{notes}
"""