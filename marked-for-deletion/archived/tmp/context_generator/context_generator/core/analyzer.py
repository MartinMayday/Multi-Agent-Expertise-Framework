"""
Dependency analyzer for import graph construction.

Builds folder-to-folder dependency relationships from import statements.
"""

from __future__ import annotations

import logging
import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .scanner import ScannedFolder
from .extractor import FileSymbols

logger = logging.getLogger(__name__)


@dataclass
class Dependency:
    """A dependency relationship."""
    source_folder: Path
    target_folder: Path
    import_count: int = 1
    import_examples: list[str] = field(default_factory=list)
    
    @property
    def is_internal(self) -> bool:
        """Check if this is an internal (same repo) dependency."""
        try:
            self.source_folder.relative_to(self.target_folder.parent)
            return True
        except ValueError:
            return False


@dataclass
class FolderDependencies:
    """Dependencies for a folder."""
    folder_path: Path
    depends_on: list[Dependency] = field(default_factory=list)
    used_by: list[Dependency] = field(default_factory=list)
    
    def internal_depends_on(self) -> list[Path]:
        """Get internal folders this folder depends on."""
        return [d.target_folder for d in self.depends_on if d.is_internal]
    
    def internal_used_by(self) -> list[Path]:
        """Get internal folders that depend on this folder."""
        return [d.source_folder for d in self.used_by if d.is_internal]


class DependencyAnalyzer:
    """Analyzes import statements to build dependency graph."""
    
    def __init__(self, root_path: Path):
        self.root_path = Path(root_path).resolve()
        self._folder_to_files: dict[Path, list[FileSymbols]] = defaultdict(list)
        self._dependencies: dict[Path, FolderDependencies] = {}
    
    def add_file_symbols(self, file_symbols: FileSymbols):
        """Add file symbols for analysis."""
        folder = file_symbols.path.parent
        self._folder_to_files[folder].append(file_symbols)
    
    def analyze(self) -> dict[Path, FolderDependencies]:
        """Analyze all collected file symbols and build dependency graph."""
        all_folders = set(self._folder_to_files.keys())
        folder_modules = self._build_folder_module_map()
        
        for folder in all_folders:
            self._dependencies[folder] = FolderDependencies(folder_path=folder)
        
        for folder, files in self._folder_to_files.items():
            for file_symbols in files:
                for import_str in file_symbols.imports:
                    target_folder = self._resolve_import(import_str, folder, folder_modules)
                    if target_folder and target_folder != folder and target_folder in all_folders:
                        self._add_dependency(folder, target_folder, import_str)
        
        return self._dependencies
    
    def _build_folder_module_map(self) -> dict[str, Path]:
        """Build map from module names to folder paths."""
        module_map = {}
        
        for folder in self._folder_to_files.keys():
            try:
                rel_path = folder.relative_to(self.root_path)
                module_name = str(rel_path).replace("/", ".").replace("\\", ".")
                module_map[module_name] = folder
                
                parts = module_name.split(".")
                for i in range(len(parts)):
                    partial = ".".join(parts[:i+1])
                    if partial not in module_map:
                        module_map[partial] = folder
            except ValueError:
                continue
        
        return module_map
    
    def _resolve_import(
        self, 
        import_str: str, 
        source_folder: Path,
        folder_modules: dict[str, Path]
    ) -> Optional[Path]:
        """Resolve an import string to a folder path."""
        import_str = import_str.strip().strip('"').strip("'")
        
        if import_str.startswith("."):
            return self._resolve_relative_import(import_str, source_folder)
        
        parts = import_str.split(".")
        for i in range(len(parts), 0, -1):
            partial = ".".join(parts[:i])
            if partial in folder_modules:
                return folder_modules[partial]
        
        for folder in self._folder_to_files.keys():
            if folder.name == parts[0]:
                return folder
        
        return None
    
    def _resolve_relative_import(self, import_str: str, source_folder: Path) -> Optional[Path]:
        """Resolve a relative import like './utils' or '../shared'."""
        levels = len(re.match(r'^\.+', import_str).group()) if import_str.startswith('.') else 0
        
        current = source_folder
        for _ in range(levels - 1):
            current = current.parent
        
        module_part = import_str.lstrip(".")
        if module_part:
            target = current / module_part.replace(".", "/")
            if target.exists():
                return target
            target = current / module_part.split(".")[0]
            if target.exists():
                return target
        
        return current if current != source_folder else None
    
    def _add_dependency(self, source: Path, target: Path, import_str: str):
        """Add a dependency relationship."""
        if source not in self._dependencies:
            self._dependencies[source] = FolderDependencies(folder_path=source)
        if target not in self._dependencies:
            self._dependencies[target] = FolderDependencies(folder_path=target)
        
        for dep in self._dependencies[source].depends_on:
            if dep.target_folder == target:
                dep.import_count += 1
                if len(dep.import_examples) < 3:
                    dep.import_examples.append(import_str)
                return
        
        self._dependencies[source].depends_on.append(Dependency(
            source_folder=source,
            target_folder=target,
            import_count=1,
            import_examples=[import_str]
        ))
        
        self._dependencies[target].used_by.append(Dependency(
            source_folder=source,
            target_folder=target,
            import_count=1,
            import_examples=[import_str]
        ))
    
    def get_folder_dependencies(self, folder: Path) -> Optional[FolderDependencies]:
        """Get dependencies for a specific folder."""
        return self._dependencies.get(folder)
    
    def get_dependency_summary(self, folder: Path) -> dict[str, list[str]]:
        """Get a human-readable dependency summary for a folder."""
        deps = self._dependencies.get(folder)
        if not deps:
            return {"depends_on": [], "used_by": []}
        
        def format_folder(path: Path) -> str:
            try:
                return str(path.relative_to(self.root_path))
            except ValueError:
                return path.name
        
        return {
            "depends_on": [format_folder(d.target_folder) for d in deps.depends_on[:10]],
            "used_by": [format_folder(d.source_folder) for d in deps.used_by[:10]]
        }
