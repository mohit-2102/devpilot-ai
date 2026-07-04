from pathlib import Path
from typing import Any
import json

from app.services.file_discovery import RepositoryDiscovery

try:
    import tomllib
except ModuleNotFoundError:
    tomllib = None


class ConfigScanner:
    """
    Scans configuration files.

    Responsibility:
    - Discover configuration files
    - Parse them when possible
    - Never infer frameworks
    """

    CONFIG_FILES = {
        "next.config.js",
        "next.config.ts",
        "vite.config.js",
        "vite.config.ts",
        "webpack.config.js",
        "webpack.config.ts",
        "tsconfig.json",
        "jsconfig.json",
        "tailwind.config.js",
        "tailwind.config.ts",
        "eslint.config.js",
        "eslint.config.mjs",
        ".eslintrc",
        ".eslintrc.json",
        ".prettierrc",
        ".prettierrc.json",
        "docker-compose.yml",
        "docker-compose.yaml",
        "Dockerfile",
        ".gitignore",
        ".gitattributes",
        ".editorconfig",
        ".env",
        ".env.example",
    }

    def scan(
        self,
        discovery: RepositoryDiscovery,
    ) -> dict[str, Any]:

        configs = []

        for file in discovery.files:

            if file.name not in self.CONFIG_FILES:
                continue

            configs.append(
                {
                    "name": file.name,
                    "path": file.relative_to(discovery.root).as_posix(),
                    "content": self._parse(file),
                }
            )

        github_workflows = self._github_workflows(discovery)

        return {
            "config_count": len(configs),
            "workflow_count": len(github_workflows),
            "config_files": configs,
            "github_workflows": github_workflows,
        }

    def _github_workflows(
        self,
        discovery: RepositoryDiscovery,
    ) -> list[dict]:

        workflows = []

        for file in discovery.files:

            parts = file.parts

            if (
                ".github" in parts
                and "workflows" in parts
            ):

                workflows.append(
                    {
                        "name": file.name,
                        "path": str(
                            file.relative_to(
                                discovery.root
                            )
                        ),
                        "content": self._read_text(file),
                    }
                )

        return workflows

    def _parse(
        self,
        file: Path,
    ) -> Any:

        suffix = file.suffix.lower()

        if suffix == ".json":
            return self._read_json(file)

        if suffix == ".toml":
            return self._read_toml(file)

        return self._read_text(file)

    def _read_json(
        self,
        file: Path,
    ):

        try:
            with open(file, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def _read_toml(
        self,
        file: Path,
    ):

        if tomllib is None:
            return {}

        try:
            with open(file, "rb") as f:
                return tomllib.load(f)
        except Exception:
            return {}

    def _read_text(
        self,
        file: Path,
    ):

        try:
            with open(
                file,
                encoding="utf-8",
                errors="ignore",
            ) as f:
                return f.read()

        except Exception:
            return ""