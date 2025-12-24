#!/usr/bin/env python3
"""
generate-context-sidecars.py

Generates AI context sidecar files (.context.md) for each source file
and folder-level index files for progressive context loading.

Based on research from:
- llms.txt protocol (llmstxt.org)
- Aider's repo-map approach (tree-sitter based)
- Codebase Context Specification

Requirements:
    pip install tree-sitter tree-sitter-python tree-sitter-javascript tree-sitter-typescript gitpython

Usage:
    python generate-context-sidecars.py /path/to/project
    python generate-context-sidecars.py /path/to/project --mode folder-index
    python generate-context-sidecars.py /path/to/project --mode sidecar
    python generate-context-sidecars.py /path/to/project --mode both
"""

import os
import sys
import json
import hashlib
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, asdict

try:
    import tree_sitter
    HAS_TREE_SITTER = True
except ImportError:
    HAS_TREE_SITTER = False
    print("Warning: tree-sitter not installed. Using basic file analysis.")

try:
    import git
    HAS_GIT = True
except ImportError:
    HAS_GIT = False


@dataclass
class FileMetadata:
    path: str
    relative_path: str
    hash: str
    lines: int
    tokens_estimate: int
    symbols: list
    imports: list
    exports: list
    relevance_score: float
    maturity_score: float
    last_modified: str
    summary: str


@dataclass
class FolderMetadata:
    path: str
    relative_path: str
    files: list
    subdirs: list
    purpose: str
    key_exports: list


LANGUAGE_EXTENSIONS = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".jsx": "javascript",
    ".rs": "rust",
    ".go": "go",
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
    ".sh": "bash",
    ".bash": "bash",
    ".zsh": "bash",
}

IGNORE_PATTERNS = [
    "__pycache__",
    "node_modules",
    ".git",
    ".venv",
    "venv",
    ".env",
    "dist",
    "build",
    ".next",
    ".nuxt",
    "coverage",
    ".pytest_cache",
    ".mypy_cache",
    "*.pyc",
    "*.pyo",
    "*.log",
    "*.lock",
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
]


def should_ignore(path: Path) -> bool:
    """Check if path should be ignored."""
    path_str = str(path)
    for pattern in IGNORE_PATTERNS:
        if pattern.startswith("*"):
            if path_str.endswith(pattern[1:]):
                return True
        elif pattern in path_str.split(os.sep):
            return True
    return False


def get_file_hash(filepath: Path) -> str:
    """Get SHA256 hash of file content."""
    content = filepath.read_bytes()
    return hashlib.sha256(content).hexdigest()[:12]


def estimate_tokens(content: str) -> int:
    """Rough token estimate (words * 1.3)."""
    words = len(content.split())
    return int(words * 1.3)


def extract_python_info(content: str, filepath: Path) -> dict:
    """Extract symbols from Python file using AST."""
    import ast
    
    symbols = []
    imports = []
    exports = []
    summary = ""
    
    try:
        tree = ast.parse(content)
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                visibility = "private" if node.name.startswith("_") else "public"
                symbols.append({
                    "name": node.name,
                    "type": "function",
                    "visibility": visibility,
                    "line": node.lineno
                })
                if visibility == "public":
                    exports.append(node.name)
                    
            elif isinstance(node, ast.AsyncFunctionDef):
                visibility = "private" if node.name.startswith("_") else "public"
                symbols.append({
                    "name": node.name,
                    "type": "async_function",
                    "visibility": visibility,
                    "line": node.lineno
                })
                if visibility == "public":
                    exports.append(node.name)
                    
            elif isinstance(node, ast.ClassDef):
                visibility = "private" if node.name.startswith("_") else "public"
                symbols.append({
                    "name": node.name,
                    "type": "class",
                    "visibility": visibility,
                    "line": node.lineno
                })
                if visibility == "public":
                    exports.append(node.name)
                    
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
                    
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
        
        module_doc = ast.get_docstring(tree)
        if module_doc:
            summary = module_doc.split("\n")[0][:200]
            
    except SyntaxError:
        pass
    
    return {
        "symbols": symbols,
        "imports": imports,
        "exports": exports,
        "summary": summary
    }


def extract_js_ts_info(content: str, filepath: Path) -> dict:
    """Extract basic info from JS/TS files (regex-based fallback)."""
    import re
    
    symbols = []
    imports = []
    exports = []
    summary = ""
    
    import_pattern = r'import\s+(?:{[^}]+}|[\w*]+)\s+from\s+[\'"]([^\'"]+)[\'"]'
    for match in re.finditer(import_pattern, content):
        imports.append(match.group(1))
    
    require_pattern = r'require\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)'
    for match in re.finditer(require_pattern, content):
        imports.append(match.group(1))
    
    func_pattern = r'(?:export\s+)?(?:async\s+)?function\s+(\w+)'
    for match in re.finditer(func_pattern, content):
        name = match.group(1)
        is_export = "export" in match.group(0)
        symbols.append({
            "name": name,
            "type": "function",
            "visibility": "public" if is_export else "private",
            "line": content[:match.start()].count("\n") + 1
        })
        if is_export:
            exports.append(name)
    
    class_pattern = r'(?:export\s+)?class\s+(\w+)'
    for match in re.finditer(class_pattern, content):
        name = match.group(1)
        is_export = "export" in match.group(0)
        symbols.append({
            "name": name,
            "type": "class",
            "visibility": "public" if is_export else "private",
            "line": content[:match.start()].count("\n") + 1
        })
        if is_export:
            exports.append(name)
    
    const_export_pattern = r'export\s+(?:const|let|var)\s+(\w+)'
    for match in re.finditer(const_export_pattern, content):
        name = match.group(1)
        exports.append(name)
        symbols.append({
            "name": name,
            "type": "variable",
            "visibility": "public",
            "line": content[:match.start()].count("\n") + 1
        })
    
    jsdoc_pattern = r'/\*\*\s*\n\s*\*\s*(.+?)(?:\n|\*/)'
    jsdoc_match = re.search(jsdoc_pattern, content)
    if jsdoc_match:
        summary = jsdoc_match.group(1).strip()[:200]
    
    return {
        "symbols": symbols,
        "imports": imports,
        "exports": exports,
        "summary": summary
    }


def calculate_relevance_score(metadata: dict, all_files: list) -> float:
    """Calculate relevance score based on various factors."""
    score = 0.5
    
    export_count = len(metadata.get("exports", []))
    if export_count > 5:
        score += 0.2
    elif export_count > 0:
        score += 0.1
    
    import_count = 0
    filepath = metadata.get("relative_path", "")
    for f in all_files:
        for imp in f.get("imports", []):
            if filepath.replace("/", ".").replace("\\", ".").rstrip(".py") in imp:
                import_count += 1
    
    if import_count > 10:
        score += 0.3
    elif import_count > 5:
        score += 0.2
    elif import_count > 0:
        score += 0.1
    
    return min(1.0, score)


def calculate_maturity_score(filepath: Path, repo_root: Optional[Path] = None) -> float:
    """Calculate maturity score based on git history and code quality."""
    score = 0.5
    
    if HAS_GIT and repo_root:
        try:
            repo = git.Repo(repo_root)
            rel_path = filepath.relative_to(repo_root)
            commits = list(repo.iter_commits(paths=str(rel_path), max_count=50))
            
            if len(commits) > 20:
                score += 0.2
            elif len(commits) > 10:
                score += 0.15
            elif len(commits) > 5:
                score += 0.1
            
            if commits:
                age_days = (datetime.now() - commits[-1].committed_datetime.replace(tzinfo=None)).days
                if age_days > 365:
                    score += 0.2
                elif age_days > 180:
                    score += 0.15
                elif age_days > 30:
                    score += 0.1
        except Exception:
            pass
    
    return min(1.0, score)


def analyze_file(filepath: Path, repo_root: Path) -> Optional[FileMetadata]:
    """Analyze a single source file."""
    if should_ignore(filepath):
        return None
    
    ext = filepath.suffix.lower()
    if ext not in LANGUAGE_EXTENSIONS:
        return None
    
    try:
        content = filepath.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return None
    
    if len(content) < 10:
        return None
    
    lang = LANGUAGE_EXTENSIONS[ext]
    
    if lang == "python":
        info = extract_python_info(content, filepath)
    elif lang in ["javascript", "typescript"]:
        info = extract_js_ts_info(content, filepath)
    else:
        info = {"symbols": [], "imports": [], "exports": [], "summary": ""}
    
    relative_path = str(filepath.relative_to(repo_root))
    
    return FileMetadata(
        path=str(filepath),
        relative_path=relative_path,
        hash=get_file_hash(filepath),
        lines=len(content.splitlines()),
        tokens_estimate=estimate_tokens(content),
        symbols=info["symbols"],
        imports=info["imports"],
        exports=info["exports"],
        relevance_score=0.5,
        maturity_score=calculate_maturity_score(filepath, repo_root),
        last_modified=datetime.fromtimestamp(filepath.stat().st_mtime).isoformat(),
        summary=info["summary"]
    )


def generate_sidecar_content(metadata: FileMetadata) -> str:
    """Generate markdown content for sidecar file."""
    lines = [
        f"# Context: {Path(metadata.relative_path).name}",
        "",
        f"**Path**: `{metadata.relative_path}`",
        f"**Lines**: {metadata.lines} | **Tokens (est)**: {metadata.tokens_estimate}",
        f"**Relevance**: {metadata.relevance_score:.2f} | **Maturity**: {metadata.maturity_score:.2f}",
        "",
    ]
    
    if metadata.summary:
        lines.extend([
            "## Summary",
            metadata.summary,
            "",
        ])
    
    if metadata.symbols:
        lines.extend([
            "## Symbols",
            "",
            "| Name | Type | Visibility | Line |",
            "|------|------|------------|------|",
        ])
        for sym in metadata.symbols[:20]:
            lines.append(
                f"| `{sym['name']}` | {sym['type']} | {sym['visibility']} | {sym.get('line', '-')} |"
            )
        if len(metadata.symbols) > 20:
            lines.append(f"| ... | ({len(metadata.symbols) - 20} more) | | |")
        lines.append("")
    
    if metadata.imports:
        lines.extend([
            "## Dependencies (imports)",
            "",
        ])
        for imp in metadata.imports[:15]:
            lines.append(f"- `{imp}`")
        if len(metadata.imports) > 15:
            lines.append(f"- ... ({len(metadata.imports) - 15} more)")
        lines.append("")
    
    if metadata.exports:
        lines.extend([
            "## Exports",
            "",
        ])
        for exp in metadata.exports[:15]:
            lines.append(f"- `{exp}`")
        if len(metadata.exports) > 15:
            lines.append(f"- ... ({len(metadata.exports) - 15} more)")
        lines.append("")
    
    lines.extend([
        "---",
        f"*Generated: {datetime.now().isoformat()}*",
    ])
    
    return "\n".join(lines)


def generate_folder_index(folder: Path, files: list[FileMetadata], repo_root: Path) -> str:
    """Generate folder-level index markdown."""
    relative_folder = folder.relative_to(repo_root) if folder != repo_root else Path(".")
    folder_name = folder.name or "Project Root"
    
    lines = [
        f"# {folder_name}",
        "",
        f"**Path**: `{relative_folder}`",
        f"**Files**: {len(files)}",
        "",
    ]
    
    extensions = {}
    for f in files:
        ext = Path(f.relative_path).suffix
        extensions[ext] = extensions.get(ext, 0) + 1
    
    if extensions:
        lines.append("## File Types")
        for ext, count in sorted(extensions.items(), key=lambda x: -x[1]):
            lines.append(f"- `{ext}`: {count} files")
        lines.append("")
    
    sorted_files = sorted(files, key=lambda x: -x.relevance_score)
    
    if sorted_files:
        lines.extend([
            "## Key Files (by relevance)",
            "",
            "| File | Lines | Relevance | Summary |",
            "|------|-------|-----------|---------|",
        ])
        for f in sorted_files[:10]:
            name = Path(f.relative_path).name
            summary = (f.summary[:50] + "...") if len(f.summary) > 50 else f.summary
            lines.append(f"| `{name}` | {f.lines} | {f.relevance_score:.2f} | {summary} |")
        lines.append("")
    
    all_exports = []
    for f in files:
        for exp in f.exports[:5]:
            all_exports.append(f"{Path(f.relative_path).stem}.{exp}")
    
    if all_exports:
        lines.extend([
            "## Exports",
            "",
        ])
        for exp in all_exports[:20]:
            lines.append(f"- `{exp}`")
        lines.append("")
    
    lines.extend([
        "---",
        f"*Generated: {datetime.now().isoformat()}*",
    ])
    
    return "\n".join(lines)


def generate_llms_txt(repo_root: Path, all_files: list[FileMetadata]) -> str:
    """Generate root llms.txt file."""
    project_name = repo_root.name
    
    readme_content = ""
    for readme_name in ["README.md", "readme.md", "README.rst", "README"]:
        readme_path = repo_root / readme_name
        if readme_path.exists():
            try:
                readme_content = readme_path.read_text()[:500]
                break
            except Exception:
                pass
    
    first_line = ""
    if readme_content:
        lines = readme_content.split("\n")
        for line in lines:
            line = line.strip()
            if line and not line.startswith("#"):
                first_line = line[:200]
                break
    
    sorted_files = sorted(all_files, key=lambda x: -x.relevance_score)[:20]
    
    lines = [
        f"# {project_name}",
        "",
    ]
    
    if first_line:
        lines.extend([
            f"> {first_line}",
            "",
        ])
    
    lines.extend([
        "## Core Files",
        "",
    ])
    
    for f in sorted_files:
        desc = f.summary[:100] if f.summary else f"({f.lines} lines)"
        lines.append(f"- [{f.relative_path}]({f.relative_path}): {desc}")
    
    lines.extend([
        "",
        "## Optional",
        "",
    ])
    
    optional_files = sorted(all_files, key=lambda x: x.relevance_score)[:10]
    for f in optional_files:
        lines.append(f"- [{f.relative_path}]({f.relative_path})")
    
    return "\n".join(lines)


def generate_manifest(repo_root: Path, all_files: list[FileMetadata]) -> dict:
    """Generate JSON manifest for programmatic access."""
    return {
        "version": "1.0",
        "generated": datetime.now().isoformat(),
        "project": repo_root.name,
        "total_files": len(all_files),
        "total_lines": sum(f.lines for f in all_files),
        "total_tokens": sum(f.tokens_estimate for f in all_files),
        "files": [asdict(f) for f in all_files]
    }


def main():
    parser = argparse.ArgumentParser(
        description="Generate AI context sidecar files for codebase"
    )
    parser.add_argument(
        "path",
        type=Path,
        help="Path to project root"
    )
    parser.add_argument(
        "--mode",
        choices=["sidecar", "folder-index", "both", "llms-txt", "manifest"],
        default="both",
        help="Generation mode"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output directory (default: .ai-context in project root)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be generated without writing files"
    )
    
    args = parser.parse_args()
    
    repo_root = args.path.resolve()
    if not repo_root.exists():
        print(f"Error: Path does not exist: {repo_root}")
        sys.exit(1)
    
    output_dir = args.output_dir or (repo_root / ".ai-context")
    
    print(f"Analyzing: {repo_root}")
    
    all_files: list[FileMetadata] = []
    
    for filepath in repo_root.rglob("*"):
        if filepath.is_file():
            metadata = analyze_file(filepath, repo_root)
            if metadata:
                all_files.append(metadata)
    
    print(f"Found {len(all_files)} source files")
    
    file_dicts = [asdict(f) for f in all_files]
    for i, f in enumerate(all_files):
        f.relevance_score = calculate_relevance_score(file_dicts[i], file_dicts)
    
    if args.dry_run:
        print("\n--- Dry Run ---")
        print(f"Would create output directory: {output_dir}")
        if args.mode in ["sidecar", "both"]:
            print(f"Would create {len(all_files)} sidecar files")
        if args.mode in ["folder-index", "both"]:
            folders = set(Path(f.relative_path).parent for f in all_files)
            print(f"Would create {len(folders)} folder index files")
        if args.mode in ["llms-txt", "both"]:
            print("Would create llms.txt")
        if args.mode in ["manifest", "both"]:
            print("Would create manifest.json")
        return
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if args.mode in ["sidecar", "both"]:
        sidecars_dir = output_dir / "sidecars"
        sidecars_dir.mkdir(exist_ok=True)
        
        for f in all_files:
            sidecar_path = sidecars_dir / (f.relative_path.replace("/", "_").replace("\\", "_") + ".context.md")
            content = generate_sidecar_content(f)
            sidecar_path.write_text(content)
        
        print(f"Generated {len(all_files)} sidecar files")
    
    if args.mode in ["folder-index", "both"]:
        folders: dict[Path, list[FileMetadata]] = {}
        for f in all_files:
            folder = Path(f.relative_path).parent
            if folder not in folders:
                folders[folder] = []
            folders[folder].append(f)
        
        index_dir = output_dir / "indexes"
        index_dir.mkdir(exist_ok=True)
        
        for folder, files in folders.items():
            folder_path = repo_root / folder
            index_content = generate_folder_index(folder_path, files, repo_root)
            
            index_filename = str(folder).replace("/", "_").replace("\\", "_") or "root"
            index_path = index_dir / f"{index_filename}.index.md"
            index_path.write_text(index_content)
        
        print(f"Generated {len(folders)} folder index files")
    
    if args.mode in ["llms-txt", "both"]:
        llms_txt = generate_llms_txt(repo_root, all_files)
        (output_dir / "llms.txt").write_text(llms_txt)
        print("Generated llms.txt")
    
    if args.mode in ["manifest", "both"]:
        manifest = generate_manifest(repo_root, all_files)
        (output_dir / "manifest.json").write_text(
            json.dumps(manifest, indent=2, default=str)
        )
        print("Generated manifest.json")
    
    print(f"\nOutput written to: {output_dir}")


if __name__ == "__main__":
    main()
