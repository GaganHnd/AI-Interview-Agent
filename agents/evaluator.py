import os
import json

from groq import Groq
from dotenv import load_dotenv
from utils.prompts import EVALUATION_PROMPT

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def evaluate_answer(role, question, answer):

    prompt = (
        EVALUATION_PROMPT
        .replace("{role}", role)
        .replace("{question}", question)
        .replace("{answer}", answer)
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0.2,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "You are an expert technical interviewer."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return json.loads(response.choices[0].message.content)