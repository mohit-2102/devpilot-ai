from abc import ABC, abstractmethod


class BaseProvider(ABC):
    """
    Abstract interface for every LLM provider.

    Every provider (Groq, Ollama, OpenRouter, etc.)
    must implement this interface.
    """

    @abstractmethod
    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate a response from the given prompt.
        """
        pass