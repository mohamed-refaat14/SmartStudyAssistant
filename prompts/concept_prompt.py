def build_concept_prompt(notes: str) -> str:
    return f"""
You are a Smart Study Assistant.

Task:
Extract the most important concepts from the lecture notes.

Requirements:
- Extract 5 to 10 key concepts.
- Each concept must have a short explanation.
- Do not add information that is not in the notes.
- Return ONLY valid JSON.
- Do not include markdown.

The JSON must follow this exact structure:

{{
    "concepts": [
        {{
            "name": "...",
            "explanation": "..."
        }}
    ]
}}

Lecture notes:
{notes}
"""