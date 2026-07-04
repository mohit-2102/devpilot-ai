from pathlib import Path
from dataclasses import dataclass, field
from typing import Any


DEFAULT_IGNORED_DIRECTORIES = {
    ".git",
    "__pycache__",
    "node_modules",
    ".next",
    "dist",
    "build",
    "target",
    ".venv",
    "venv",
    ".idea",
    ".vscode",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
}

DEFAULT_IGNORED_FILES = {
    ".DS_Store",
    "Thumbs.db",
}

@dataclass
class RepositoryDiscovery:

    root: Path

    files: list[Path] = field(default_factory=list)

    directories: list[Path] = field(default_factory=list)

    tree: dict[str, Any] | None = None


class FileDiscovery:

    def __init__(
        self,
        repo_path: str,
        ignored_directories: set[str] | None = None,
    ):

        self.root = Path(repo_path).resolve()

        self.ignored = (
        ignored_directories
        or DEFAULT_IGNORED_DIRECTORIES
        )

        self.ignored_files = set(DEFAULT_IGNORED_FILES)

    def discover(self) -> RepositoryDiscovery:

        discovery = RepositoryDiscovery(root=self.root)

        discovery.tree = self._build_tree(
            self.root,
            discovery,
        )

        discovery.files.sort(key=lambda p: p.as_posix())
        discovery.directories.sort(key=lambda p: p.as_posix())

        return discovery

    def _build_tree(
        self,
        directory: Path,
        discovery: RepositoryDiscovery,
    ) -> dict[str, Any]:

        node = {
            "name": directory.name,
            "type": "directory",
            "children": [],
        }

        if directory != self.root:
            discovery.directories.append(directory)

        try:

            entries = sorted(
                directory.iterdir(),
                key=lambda item: (
                    item.is_file(),
                    item.name.lower(),
                ),
            )

        except PermissionError:
            return node

        for entry in entries:

            if self._should_ignore(entry):
                continue

            if entry.is_dir():

                node["children"].append(
                    self._build_tree(
                        entry,
                        discovery,
                    )
                )

            else:

                discovery.files.append(entry)

                node["children"].append(
                    {
                        "name": entry.name,
                        "type": "file",
                    }
                )

        return node

    def _should_ignore(self, path: Path) -> bool:

        if path.name in self.ignored_files:
            return True

        for part in path.parts:
            if part in self.ignored:
                return True

        return False