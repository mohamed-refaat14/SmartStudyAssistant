def build_mcq_prompt(notes: str) -> str:
    return f"""
You are a Smart Study Assistant.

Task:
Generate multiple-choice questions from the lecture notes.

Requirements:
- Generate 5 MCQs.
- Each question must have 4 choices: A, B, C, D.
- Mark the correct answer after each question.
- Add a short explanation.
- Do not add information that is not in the notes.

Format:
Question 1:
A)

B)

C)

D)
Correct answer:
Explanation:

Lecture notes:
{notes}
"""