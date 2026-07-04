from typing import Any

from app.services.file_discovery import FileDiscovery

from app.services.scanners.filesystem_scanner import FileSystemScanner
from app.services.scanners.manifest_scanner import ManifestScanner
from app.services.scanners.documentation_scanner import DocumentationScanner
from app.services.scanners.source_scanner import SourceScanner
from app.services.scanners.config_scanner import ConfigScanner
from app.services.scanners.metadata_scanner import MetadataScanner
from app.schemas.repository_schema import RepositoryIndex


class RepositoryAnalyzer:
    """
    Main orchestration service.

    Coordinates every scanner and produces
    one Repository Index.
    """

    def __init__(self, repo_path: str):
        self.repo_path = repo_path

    from app.schemas.repository_schema import RepositoryIndex
    def analyze(self) -> RepositoryIndex:

        # Discover repository once
        discovery = FileDiscovery(
            self.repo_path
        ).discover()

        # Run scanners
        filesystem = FileSystemScanner().scan(discovery)

        manifests = ManifestScanner().scan(discovery)

        documentation = DocumentationScanner().scan(discovery)

        source = SourceScanner().scan(discovery)

        configs = ConfigScanner().scan(discovery)

        metadata = MetadataScanner().scan(discovery)

        # Final Repository Index
        return RepositoryIndex(
        metadata=metadata,
        filesystem=filesystem,
        manifests=manifests,
        documentation=documentation,
        source=source,
        configs=configs,
        )