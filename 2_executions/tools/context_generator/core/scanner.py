"""
File scanner with .gitignore support.

Recursively scans directories and respects .gitignore patterns.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator, Optional

import pathspec

logger = logging.getLogger(__name__)

SUPPORTED_EXTENSIONS = {
    # Programming languages
    ".py": "python",
    ".pyi": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".go": "go",
    ".rs": "rust",
    ".java": "java",
    ".c": "c",
    ".cpp": "cpp",
    ".h": "c",
    ".hpp": "cpp",
    ".rb": "ruby",
    ".php": "php",
    ".swift": "swift",
    ".kt": "kotlin",
    ".scala": "scala",
    ".cs": "csharp",
    
    # Web frameworks
    ".vue": "vue",
    ".svelte": "svelte",
    
    # Documentation and text files
    ".md": "markdown",
    ".txt": "text",
    ".rst": "rst",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".toml": "toml",
    ".json": "json",
    ".xml": "xml",
    ".sh": "shell",
    ".bash": "shell",
    ".zsh": "shell",
}

DEFAULT_IGNORE_PATTERNS = [
    "__pycache__/",
    "*.pyc",
    ".git/",
    "node_modules/",
    ".venv/",
    "venv/",
    ".env/",
    "dist/",
    "build/",
    ".next/",
    ".nuxt/",
    "*.egg-info/",
    ".pytest_cache/",
    ".mypy_cache/",
    ".ruff_cache/",
    "*.min.js",
    "*.bundle.js",
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "Cargo.lock",
    "poetry.lock",
]


@dataclass
class ScannedFile:
    """Information about a scanned file."""
    path: Path
    relative_path: Path
    language: str
    size_bytes: int
    estimated_tokens: int
    
    @property
    def extension(self) -> str:
        return self.path.suffix.lower()


@dataclass
class ScannedFolder:
    """Information about a scanned folder."""
    path: Path
    relative_path: Path
    files: list[ScannedFile] = field(default_factory=list)
    subfolders: list[str] = field(default_factory=list)
    readme_path: Optional[Path] = None
    
    @property
    def total_files(self) -> int:
        return len(self.files)
    
    @property
    def total_tokens(self) -> int:
        return sum(f.estimated_tokens for f in self.files)
    
    @property
    def languages(self) -> set[str]:
        return {f.language for f in self.files}


class FileScanner:
    """Scans directories for source files respecting .gitignore."""
    
    def __init__(
        self,
        root_path: Path,
        max_depth: int = 10,
        additional_ignore: Optional[list[str]] = None
    ):
        self.root_path = Path(root_path).resolve()
        self.max_depth = max_depth
        self._ignore_spec = self._build_ignore_spec(additional_ignore)
    
    def _build_ignore_spec(self, additional: Optional[list[str]] = None) -> pathspec.PathSpec:
        """Build pathspec from .gitignore and defaults."""
        patterns = list(DEFAULT_IGNORE_PATTERNS)
        
        if additional:
            patterns.extend(additional)
        
        gitignore_path = self.root_path / ".gitignore"
        if gitignore_path.exists():
            with open(gitignore_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        patterns.append(line)
        
        return pathspec.PathSpec.from_lines("gitwildmatch", patterns)
    
    def _is_ignored(self, path: Path) -> bool:
        """Check if path should be ignored."""
        try:
            rel_path = path.relative_to(self.root_path)
            rel_str = str(rel_path)
            if path.is_dir():
                rel_str += "/"
            return self._ignore_spec.match_file(rel_str)
        except ValueError:
            return True
    
    def _estimate_tokens(self, path: Path) -> int:
        """Estimate token count (chars / 4 approximation)."""
        try:
            size = path.stat().st_size
            return max(1, size // 4)
        except OSError:
            return 0
    
    def _get_language(self, path: Path) -> str:
        """Get language from file extension."""
        return SUPPORTED_EXTENSIONS.get(path.suffix.lower(), "unknown")
    
    def scan_file(self, path: Path) -> Optional[ScannedFile]:
        """Scan a single file and return its info."""
        if not path.is_file():
            return None
        
        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            return None
        
        if self._is_ignored(path):
            return None
        
        try:
            rel_path = path.relative_to(self.root_path)
            return ScannedFile(
                path=path,
                relative_path=rel_path,
                language=self._get_language(path),
                size_bytes=path.stat().st_size,
                estimated_tokens=self._estimate_tokens(path)
            )
        except Exception as e:
            logger.warning(f"Error scanning {path}: {e}")
            return None
    
    def scan_folder(self, folder_path: Path) -> Optional[ScannedFolder]:
        """Scan a folder and return its info (non-recursive for files)."""
        folder_path = Path(folder_path).resolve()
        
        if not folder_path.is_dir():
            return None
        
        if self._is_ignored(folder_path):
            return None
        
        try:
            rel_path = folder_path.relative_to(self.root_path)
        except ValueError:
            rel_path = Path(".")
        
        files = []
        subfolders = []
        readme_path = None
        
        try:
            for item in folder_path.iterdir():
                if self._is_ignored(item):
                    continue
                
                if item.is_dir():
                    subfolders.append(item.name)
                elif item.is_file():
                    if item.name.lower() in ("readme.md", "readme.txt", "readme"):
                        readme_path = item
                    
                    scanned = self.scan_file(item)
                    if scanned:
                        files.append(scanned)
        except PermissionError:
            logger.warning(f"Permission denied: {folder_path}")
        
        return ScannedFolder(
            path=folder_path,
            relative_path=rel_path,
            files=sorted(files, key=lambda f: f.path.name),
            subfolders=sorted(subfolders),
            readme_path=readme_path
        )
    
    def scan_all_folders(self, min_files: int = 1) -> Iterator[ScannedFolder]:
        """
        Recursively scan all folders that contain source files.
        
        Args:
            min_files: Minimum files required to include a folder
        
        Yields:
            ScannedFolder for each qualifying folder
        """
        def _scan_recursive(path: Path, depth: int) -> Iterator[ScannedFolder]:
            if depth > self.max_depth:
                return
            
            folder = self.scan_folder(path)
            if folder is None:
                return
            
            if folder.total_files >= min_files:
                yield folder
            
            for subfolder_name in folder.subfolders:
                subfolder_path = path / subfolder_name
                yield from _scan_recursive(subfolder_path, depth + 1)
        
        yield from _scan_recursive(self.root_path, 0)
