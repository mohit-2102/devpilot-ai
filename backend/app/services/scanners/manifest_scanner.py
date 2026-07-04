from pathlib import Path
from typing import Any
import json

from app.services.file_discovery import RepositoryDiscovery

try:
    import tomllib
except ModuleNotFoundError:
    tomllib = None


class ManifestScanner:

    MANIFESTS = {
        "package.json": "_package_json",
        "requirements.txt": "_requirements",
        "pyproject.toml": "_toml",
        "Cargo.toml": "_toml",
        "composer.json": "_json",
        "go.mod": "_text",
        "pom.xml": "_text",
        "build.gradle": "_text",
        "build.gradle.kts": "_text",
        "Gemfile": "_text",
        "CMakeLists.txt": "_text",
        "Makefile": "_text",
        "meson.build": "_text",
        "vcpkg.json": "_json",
        "pubspec.yaml": "_text",
    }

    def scan(
        self,
        discovery: RepositoryDiscovery,
    ) -> dict[str, Any]:

        manifests = []

        for file in discovery.files:

            parser_name = self.MANIFESTS.get(file.name)

            if parser_name is None:
                continue

            parser = getattr(self, parser_name)

            manifests.append(
                {
                    "name": file.name,
                    "path": file.relative_to(discovery.root).as_posix(),
                    "content": parser(file),
                }
            )

        return {
            "manifest_count": len(manifests),
            "manifests": manifests,
        }

    def _package_json(self, file: Path):

        try:

            with open(file, encoding="utf-8") as f:
                data = json.load(f)

            return {
                "dependencies": data.get("dependencies", {}),
                "devDependencies": data.get("devDependencies", {}),
                "scripts": data.get("scripts", {}),
            }

        except Exception:
            return {}

    def _requirements(self, file: Path):

        try:

            with open(file, encoding="utf-8") as f:

                return [
                    line.strip()
                    for line in f.readlines()
                    if line.strip()
                    and not line.startswith("#")
                ]

        except Exception:
            return []

    def _json(self, file: Path):

        try:

            with open(file, encoding="utf-8") as f:
                return json.load(f)

        except Exception:
            return {}

    def _toml(self, file: Path):

        if tomllib is None:
            return {}

        try:

            with open(file, "rb") as f:
                return tomllib.load(f)

        except Exception:
            return {}

    def _text(self, file: Path):

        try:

            with open(
                file,
                encoding="utf-8",
                errors="ignore",
            ) as f:
                return f.read()

        except Exception:
            return ""