def build_summary_prompt(notes: str) -> str:
    return f"""
You are a Smart Study Assistant.

Task:
Summarize the following lecture notes clearly for a university student.

Requirements:
- Keep the summary clear.
- Focus on the most important ideas.
- Use bullet points.
- Do not add information that is not in the notes.

Lecture notes:
{notes}
"""