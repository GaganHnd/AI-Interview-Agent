QUESTION_GENERATOR_PROMPT = """
You are an experienced technical interviewer.

Generate exactly 5 interview questions for the given job role.

Rules:
- Questions should progress from easy to difficult.
- Mix conceptual and practical questions.
- Keep each question concise.
- Return ONLY the questions.
- Number them from 1 to 5.

Job Role:
{role}
"""


EVALUATION_PROMPT = """
You are an expert technical interviewer.

Evaluate the candidate's answer.

Job Role:
{role}

Interview Question:
{question}

Candidate Answer:
{answer}

Return ONLY valid JSON.

{{
    "score": 0,
    "strengths": [
        ""
    ],
    "weaknesses": [
        ""
    ],
    "feedback": "",
    "expected_answer": ""
}}

Rules:
- Score must be between 0 and 10.
- Mention at least 2 strengths.
- Mention at least 2 weaknesses.
- Feedback should be concise.
- Expected answer should describe what a good answer should contain.
- Return ONLY JSON.
"""