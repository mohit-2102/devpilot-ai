from pathlib import Path
from typing import Any
from collections import Counter

from app.services.file_discovery import RepositoryDiscovery


class MetadataScanner:
    """
    Collects repository-level statistics.

    Does NOT parse code.
    Does NOT call AI.
    """

    def scan(
        self,
        discovery: RepositoryDiscovery,
    ) -> dict[str, Any]:

        root = discovery.root

        total_files = len(discovery.files)
        total_directories = len(discovery.directories)

        total_size = 0

        extension_counter = Counter()

        largest_files = []

        max_depth = 0

        hidden_files = 0

        for file in discovery.files:

            try:
                size = file.stat().st_size
            except OSError:
                continue

            total_size += size

            extension = file.suffix.lower()

            if extension:
                extension_counter[extension] += 1

            if file.name.startswith("."):
                hidden_files += 1

            depth = len(file.relative_to(root).parts)

            if depth > max_depth:
                max_depth = depth

            largest_files.append(
                {
                    "path": file.relative_to(discovery.root).as_posix(),
                    "size": size,
                }
            )

        largest_files.sort(
            key=lambda item: item["size"],
            reverse=True,
        )

        return {
            "repository_name": root.name,
            "total_files": total_files,
            "total_directories": total_directories,
            "repository_size_bytes": total_size,
            "repository_size_mb": round(
                total_size / (1024 * 1024),
                2,
            ),
            "maximum_depth": max_depth,
            "hidden_files": hidden_files,
            "largest_files": largest_files[:10],
            "file_extension_distribution": dict(
                extension_counter
            ),
        }