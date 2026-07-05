from app.services.context_builder import ContextBuilder
from app.services.prompt_builder import PromptBuilder
from app.services.providers.groq_provider import GroqProvider


class LLMService:
    """
    Coordinates the complete AI pipeline.

    RepositoryIndex
        ↓
    ContextBuilder
        ↓
    PromptBuilder
        ↓
    LLM Provider
    """

    def __init__(self):

        # Later this can come from config/settings
        self.provider = GroqProvider()

    def generate(
        self,
        repository_index: dict,
        task: str,
        user_query: str | None = None,
        file_path: str | None = None,
    ) -> str:

        context = ContextBuilder(
            repository_index=repository_index,
            task=task,
            file_path=file_path,
        ).build()

        prompt = PromptBuilder(
            task=task,
            context=context,
            user_query=user_query,
        ).build()

        return self.provider.generate(prompt)