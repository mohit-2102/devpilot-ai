from collections import defaultdict
from typing import Any

from app.services.file_discovery import RepositoryDiscovery


class SourceScanner:

    LANGUAGE_MAP = {
        ".py": "Python",
        ".js": "JavaScript",
        ".jsx": "JavaScript",
        ".ts": "TypeScript",
        ".tsx": "TypeScript",
        ".java": "Java",
        ".kt": "Kotlin",
        ".c": "C",
        ".cpp": "C++",
        ".cc": "C++",
        ".cxx": "C++",
        ".h": "C/C++ Header",
        ".hpp": "C++ Header",
        ".cs": "C#",
        ".go": "Go",
        ".rs": "Rust",
        ".swift": "Swift",
        ".php": "PHP",
        ".rb": "Ruby",
        ".scala": "Scala",
        ".dart": "Dart",
        ".m": "Objective-C",
        ".mm": "Objective-C++",
    }

    ENTRY_POINTS = {
        "main.py",
        "app.py",
        "manage.py",
        "main.ts",
        "main.tsx",
        "index.ts",
        "index.tsx",
        "index.js",
        "index.jsx",
        "server.js",
        "server.ts",
        "Program.cs",
        "main.cpp",
        "main.c",
        "Main.java",
        "main.go",
        "main.rs",
    }

    def scan(
        self,
        discovery: RepositoryDiscovery,
    ) -> dict[str, Any]:
        source_files = []
        languages = defaultdict(
            lambda: {
                "extensions": set(),
                "files": [],
            }
        )

        entry_points = []

        for file in discovery.files:

            extension = file.suffix.lower()

            language = self.LANGUAGE_MAP.get(extension)

            if language is None:
                continue

            relative = file.relative_to(discovery.root).as_posix()
            source_files.append(relative)

            languages[language]["extensions"].add(extension)
            languages[language]["files"].append(relative)

            if file.name in self.ENTRY_POINTS:
                entry_points.append(relative)

        result = {}

        total = 0

        for language, data in languages.items():

            result[language] = {
                "extensions": sorted(
                    data["extensions"]
                ),
                "file_count": len(
                    data["files"]
                ),
                "files": sorted(
                    data["files"]
                ),
            }

            total += len(data["files"])

            return {
                "source_files": sorted(source_files),
                "languages": result,
                "entry_points": sorted(entry_points),
                "total_source_files": total,
            }