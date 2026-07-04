from typing import Any

from app.services.file_discovery import RepositoryDiscovery


class FileSystemScanner:
    """
    Returns filesystem information collected during discovery.
    """

    def scan(
        self,
        discovery: RepositoryDiscovery,
    ) -> dict[str, Any]:

        return {
            "folder_tree": discovery.tree,
            "files": [
                file.relative_to(discovery.root).as_posix()
                for file in discovery.files
            ],
            "directories": [
                str(directory.relative_to(discovery.root))
                for directory in discovery.directories
            ],
        }