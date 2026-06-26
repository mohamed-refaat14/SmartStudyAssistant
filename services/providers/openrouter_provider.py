import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("OPENROUTER_MODEL", "openrouter/free")

API_URL = "https://openrouter.ai/api/v1/chat/completions"


def generate(prompt: str) -> str:
    if not API_KEY:
        raise ValueError("OPENROUTER_API_KEY is missing. Add it to your .env file.")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
    }

    response = requests.post(
        API_URL,
        headers=headers,
        json=payload,
        timeout=60,
    )

    if response.status_code != 200:
        raise Exception(
            f"OpenRouter API error: {response.status_code}\n{response.text}"
        )

    data = response.json()

    return data["choices"][0]["message"]["content"]