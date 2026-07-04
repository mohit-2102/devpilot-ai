from typing import Any

from pydantic import BaseModel, Field


# -------------------------
# Metadata
# -------------------------

class LargestFile(BaseModel):
    path: str
    size: int


class Metadata(BaseModel):
    repository_name: str
    total_files: int
    total_directories: int
    repository_size_bytes: int
    repository_size_mb: float
    maximum_depth: int
    hidden_files: int
    largest_files: list[LargestFile]
    file_extension_distribution: dict[str, int]


# -------------------------
# Filesystem
# -------------------------

class FileTreeNode(BaseModel):
    name: str
    type: str
    children: list["FileTreeNode"] = Field(default_factory=list)


FileTreeNode.model_rebuild()


class FileSystem(BaseModel):
    folder_tree: FileTreeNode
    files: list[str]
    directories: list[str]


# -------------------------
# Manifest
# -------------------------

class Manifest(BaseModel):
    name: str
    path: str
    content: Any


class ManifestCollection(BaseModel):
    manifests: list[Manifest]


# -------------------------
# Documentation
# -------------------------

class Documentation(BaseModel):
    name: str
    path: str
    content: str


class DocumentationCollection(BaseModel):
    documentation: list[Documentation]


# -------------------------
# Languages
# -------------------------

class Language(BaseModel):
    extensions: list[str]
    file_count: int
    files: list[str]


class Source(BaseModel):
    languages: dict[str, Language]
    entry_points: list[str]
    total_source_files: int


# -------------------------
# Config
# -------------------------

class ConfigFile(BaseModel):
    name: str
    path: str
    content: Any


class Config(BaseModel):
    config_files: list[ConfigFile]
    github_workflows: list[ConfigFile]


# -------------------------
# Final Repository Index
# -------------------------

class RepositoryIndex(BaseModel):
    metadata: Metadata
    filesystem: FileSystem
    manifests: ManifestCollection
    documentation: DocumentationCollection
    source: Source
    configs: Config