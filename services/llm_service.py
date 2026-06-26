import os

from dotenv import load_dotenv

load_dotenv()

provider = os.getenv("LLM_PROVIDER", "mock").lower()
print(f"Provider = {provider}")

def ask_llm(prompt: str) -> str:
    if not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    if provider == "mock":
        from services.providers.mock_provider import generate

        return generate(prompt)

    if provider == "openrouter":
        from services.providers.openrouter_provider import generate

        return generate(prompt)

    raise ValueError(f"Unknown LLM_PROVIDER: {provider}")