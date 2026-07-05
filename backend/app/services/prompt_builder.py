from app.services.prompts.architecture_prompt import architecture_prompt
from app.services.prompts.readme_prompt import readme_prompt
from app.services.prompts.documentation_prompt import documentation_prompt
from app.services.prompts.explain_file_prompt import explain_file_prompt
from app.services.prompts.qa_prompt import qa_prompt


class PromptBuilder:
    """
    Combines:

    - Task Prompt
    - Repository Context
    - Optional User Query

    into one final prompt.
    """

    def __init__(
        self,
        task: str,
        context: dict,
        user_query: str | None = None,
    ):

        self.task = task
        self.context = context
        self.user_query = user_query

    def build(self) -> str:

        builders = {
            "architecture": architecture_prompt,
            "readme": readme_prompt,
            "documentation": documentation_prompt,
            "explain_file": explain_file_prompt,
            "qa": qa_prompt,
        }

        builder = builders.get(self.task)

        if builder is None:
            raise ValueError(
                f"Unsupported task: {self.task}"
            )

        return builder(
            context=self.context,
            user_query=self.user_query,
        )