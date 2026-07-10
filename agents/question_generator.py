import os
from groq import Groq
from dotenv import load_dotenv

from utils.prompts import QUESTION_GENERATOR_PROMPT

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_questions(role: str):
    prompt = QUESTION_GENERATOR_PROMPT.format(role=role)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are an expert technical interviewer."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
    )

    text = response.choices[0].message.content

    questions = []

    for line in text.split("\n"):
        line = line.strip()

        if not line:
            continue

        if line[0].isdigit():
            question = line.split(".", 1)[-1].strip()
            questions.append(question)

    return questions