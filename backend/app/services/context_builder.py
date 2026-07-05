from typing import Any


class ContextBuilder:
    """
    Converts a RepositoryIndex into a task-specific,
    LLM-ready context.

    This class NEVER calls an LLM.
    """

    def __init__(
        self,
        repository_index: dict[str, Any],
        task: str,
        file_path: str | None = None,
    ):

        self.index = repository_index
        self.task = task
        self.file_path = file_path

    def build(self) -> dict[str, Any]:

        builders = {
            "architecture": self._architecture_context,
            "readme": self._readme_context,
            "documentation": self._documentation_context,
            "explain_file": self._file_context,
            "qa": self._qa_context,
        }

        builder = builders.get(self.task)

        if builder is None:
            raise ValueError(f"Unsupported task: {self.task}")

        return builder()

    # =====================================================
    # Shared Context
    # =====================================================

    def _base_context(self):

        return {
            "project": self._project(),
            "languages": self._languages(),
            "dependencies": self._dependencies(),
            "entry_points": self._entry_points(),
        }

    def _project(self):

        metadata = self.index["metadata"]

        return {
            "name": metadata["repository_name"],
            "total_files": metadata["total_files"],
            "total_directories": metadata["total_directories"],
        }

    def _languages(self):

        return self.index["source"]["languages"]

    def _dependencies(self):

        manifests = self.index["manifests"]["manifests"]

        dependencies = {}

        for manifest in manifests:

            content = manifest["content"]

            if isinstance(content, dict):

                dependencies[manifest["name"]] = {
                    "dependencies": content.get(
                        "dependencies",
                        {}
                    ),
                    "devDependencies": content.get(
                        "devDependencies",
                        {}
                    ),
                    "scripts": content.get(
                        "scripts",
                        {}
                    ),
                }

        return dependencies

    def _entry_points(self):

        return self.index["source"]["entry_points"]

    # =====================================================
    # Architecture
    # =====================================================

    def _architecture_context(self):

        context = self._base_context()

        context["folder_tree"] = self.index["filesystem"][
            "folder_tree"
        ]

        context["configs"] = self._configs()

        return context

    # =====================================================
    # README
    # =====================================================

    def _readme_context(self):

        context = self._base_context()

        context["documentation"] = self._documentation()

        context["folder_tree"] = self.index["filesystem"][
            "folder_tree"
        ]

        return context

    # =====================================================
    # Documentation
    # =====================================================

    def _documentation_context(self):

        context = self._base_context()

        context["documentation"] = self._documentation()

        context["configs"] = self._configs()

        return context

    # =====================================================
    # Explain File
    # =====================================================

    def _file_context(self):

        context = self._base_context()

        context["target_file"] = self.file_path

        return context

    # =====================================================
    # Repository QA
    # =====================================================

    def _qa_context(self):

        context = self._base_context()

        context["folder_tree"] = self.index["filesystem"][
            "folder_tree"
        ]

        context["documentation"] = self._documentation()

        context["configs"] = self._configs()

        return context

    # =====================================================
    # Helpers
    # =====================================================

    def _documentation(self):

        docs = []

        for document in self.index["documentation"][
            "documentation"
        ]:

            docs.append(
                {
                    "name": document["name"],
                    "path": document["path"],
                    "content": document["content"][:4000],
                }
            )

        return docs

    def _configs(self):

        configs = []

        for config in self.index["configs"][
            "config_files"
        ]:

            configs.append(
                {
                    "name": config["name"],
                    "path": config["path"],
                }
            )

        return configs