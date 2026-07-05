import os

from groq import Groq

from app.services.providers.base_provider import BaseProvider


class GroqProvider(BaseProvider):
    """
    Groq LLM Provider.
    """

    DEFAULT_MODEL = "llama-3.3-70b-versatile"

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
    ):

        self.api_key = api_key or os.getenv("GROQ_API_KEY")

        if not self.api_key:
            raise ValueError(
                "GROQ_API_KEY environment variable not found."
            )

        self.model = model or self.DEFAULT_MODEL

        self.client = Groq(
            api_key=self.api_key
        )

    def generate(
        self,
        prompt: str,
    ) -> str:

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.2,
        )

        return response.choices[0].message.content.strip()