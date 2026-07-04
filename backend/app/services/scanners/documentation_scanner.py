from pathlib import Path
from typing import Any

from app.services.file_discovery import RepositoryDiscovery


class DocumentationScanner:

    DOCUMENTATION_FILES = {
        "README.md",
        "README",
        "LICENSE",
        "CHANGELOG.md",
        "CONTRIBUTING.md",
        "CODE_OF_CONDUCT.md",
        "SECURITY.md",
    }

    def scan(
        self,
        discovery: RepositoryDiscovery,
    ) -> dict[str, Any]:

        documentation = []

        for file in discovery.files:

            if file.name not in self.DOCUMENTATION_FILES:
                continue

            documentation.append(
                {
                    "name": file.name,
                    "path": file.relative_to(discovery.root).as_posix(),
                    "content": self._read(file),
                }
            )

        return {
            "documentation_count": len(documentation),
            "documentation": documentation,
        }

    def _read(
        self,
        file: Path,
    ) -> str:

        try:
            with open(
                file,
                encoding="utf-8",
                errors="ignore",
            ) as f:
                return f.read()

        except Exception:
            return ""