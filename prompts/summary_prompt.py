def build_summary_prompt(notes: str) -> str:
    return f"""
You are a Smart Study Assistant.

Task:
Summarize the lecture notes clearly for a university student.

Requirements:
- Focus on the most important ideas.
- Use clear bullet points inside the summary string.
- Do not add information that is not in the notes.
- Return ONLY valid JSON.
- Do not include markdown.
- from 100 to 200 words.

The JSON must follow this exact structure:

{{
    "summary": "..."
}}

Lecture notes:
{notes}
"""