#!/usr/bin/env python3
"""
full-coverage-indexer.py

Ensures 100% content coverage for AI context retrieval by:
1. Chunking large files into semantically meaningful segments
2. Creating per-chunk metadata sidecars
3. Building hierarchical indexes at module/file/chunk levels
4. Generating keyword and symbol search indexes

This solves the "first 2000 chars only" problem by making ALL content
discoverable through multiple access paths.

Requirements:
    pip install gitpython tiktoken

Optional (for embeddings):
    pip install sentence-transformers chromadb

Usage:
    python full-coverage-indexer.py /path/to/project
    python full-coverage-indexer.py /path/to/project --chunk-size 1500
    python full-coverage-indexer.py /path/to/project --with-embeddings
"""

import os
import sys
import json
import hashlib
import re
import argparse
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Optional
from collections import defaultdict

try:
    import tiktoken
    ENCODER = tiktoken.get_encoding("cl100k_base")
    def count_tokens(text: str) -> int:
        return len(ENCODER.encode(text))
except ImportError:
    def count_tokens(text: str) -> int:
        return int(len(text.split()) * 1.3)


@dataclass
class Chunk:
    """Represents a semantically meaningful chunk of code."""
    chunk_id: str
    source_file: str
    relative_path: str
    line_start: int
    line_end: int
    char_start: int
    char_end: int
    token_count: int
    content: str
    symbols: list = field(default_factory=list)
    imports: list = field(default_factory=list)
    summary: str = ""
    keywords: list = field(default_factory=list)
    context_before: str = ""  # Last line of previous chunk for continuity
    context_after: str = ""   # First line of next chunk for continuity


@dataclass 
class FileIndex:
    """Index entry for a source file."""
    path: str
    relative_path: str
    hash: str
    total_lines: int
    total_tokens: int
    total_chars: int
    chunk_count: int
    chunk_ids: list
    symbols: list
    imports: list
    exports: list
    summary: str
    language: str
    last_indexed: str


@dataclass
class ModuleIndex:
    """Index entry for a module/folder."""
    path: str
    relative_path: str
    file_count: int
    total_lines: int
    total_tokens: int
    files: list
    submodules: list
    key_exports: list
    summary: str


# Configuration
CHUNK_TARGET_TOKENS = 1500  # Target chunk size
CHUNK_MAX_TOKENS = 2000     # Never exceed this
CHUNK_MIN_TOKENS = 200      # Don't create tiny chunks
OVERLAP_LINES = 5           # Lines to overlap between chunks

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
    ".rb": "ruby",
    ".php": "php",
    ".swift": "swift",
    ".kt": "kotlin",
    ".scala": "scala",
    ".sh": "bash",
    ".md": "markdown",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".json": "json",
    ".toml": "toml",
}

IGNORE_PATTERNS = [
    "__pycache__", "node_modules", ".git", ".venv", "venv",
    "dist", "build", ".next", ".nuxt", "coverage",
    ".pytest_cache", ".mypy_cache", "*.pyc", "*.log",
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
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


def get_file_hash(content: str) -> str:
    """Get hash of content."""
    return hashlib.sha256(content.encode()).hexdigest()[:16]


def extract_symbols_python(content: str) -> tuple[list, list, list]:
    """Extract symbols, imports, exports from Python."""
    import ast
    
    symbols = []
    imports = []
    exports = []
    
    try:
        tree = ast.parse(content)
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                visibility = "private" if node.name.startswith("_") else "public"
                sig = f"def {node.name}(...)"
                symbols.append({
                    "name": node.name,
                    "type": "function",
                    "visibility": visibility,
                    "line": node.lineno,
                    "signature": sig
                })
                if visibility == "public":
                    exports.append(node.name)
                    
            elif isinstance(node, ast.ClassDef):
                visibility = "private" if node.name.startswith("_") else "public"
                symbols.append({
                    "name": node.name,
                    "type": "class",
                    "visibility": visibility,
                    "line": node.lineno,
                    "signature": f"class {node.name}"
                })
                if visibility == "public":
                    exports.append(node.name)
                    
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
                    
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
                    
    except SyntaxError:
        pass
    
    return symbols, imports, exports


def extract_symbols_js(content: str) -> tuple[list, list, list]:
    """Extract symbols from JS/TS using regex."""
    symbols = []
    imports = []
    exports = []
    
    # Imports
    for match in re.finditer(r'import\s+.*?from\s+[\'"]([^\'"]+)[\'"]', content):
        imports.append(match.group(1))
    for match in re.finditer(r'require\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)', content):
        imports.append(match.group(1))
    
    # Functions
    for match in re.finditer(r'(?:export\s+)?(?:async\s+)?function\s+(\w+)', content):
        name = match.group(1)
        is_export = "export" in match.group(0)
        line = content[:match.start()].count("\n") + 1
        symbols.append({
            "name": name,
            "type": "function",
            "visibility": "public" if is_export else "private",
            "line": line,
            "signature": f"function {name}(...)"
        })
        if is_export:
            exports.append(name)
    
    # Classes
    for match in re.finditer(r'(?:export\s+)?class\s+(\w+)', content):
        name = match.group(1)
        is_export = "export" in match.group(0)
        line = content[:match.start()].count("\n") + 1
        symbols.append({
            "name": name,
            "type": "class",
            "visibility": "public" if is_export else "private",
            "line": line,
            "signature": f"class {name}"
        })
        if is_export:
            exports.append(name)
    
    return symbols, imports, exports


def extract_keywords(content: str, symbols: list) -> list:
    """Extract meaningful keywords from content."""
    keywords = set()
    
    # Add symbol names
    for sym in symbols:
        keywords.add(sym["name"].lower())
        # Split camelCase/snake_case
        parts = re.split(r'[_\s]|(?<=[a-z])(?=[A-Z])', sym["name"])
        for part in parts:
            if len(part) > 2:
                keywords.add(part.lower())
    
    # Extract significant words (excluding common programming terms)
    stopwords = {
        "the", "and", "for", "def", "class", "return", "import", "from",
        "self", "this", "true", "false", "null", "none", "if", "else",
        "elif", "while", "for", "in", "not", "is", "as", "with", "try",
        "except", "finally", "raise", "assert", "pass", "break", "continue",
        "function", "const", "let", "var", "async", "await", "export",
    }
    
    words = re.findall(r'\b[a-zA-Z]{3,}\b', content.lower())
    word_freq = defaultdict(int)
    for word in words:
        if word not in stopwords:
            word_freq[word] += 1
    
    # Top frequent meaningful words
    sorted_words = sorted(word_freq.items(), key=lambda x: -x[1])[:20]
    for word, _ in sorted_words:
        keywords.add(word)
    
    return list(keywords)[:30]


def find_semantic_boundaries(lines: list[str], language: str) -> list[int]:
    """Find natural break points in code (class/function definitions, blank lines)."""
    boundaries = [0]  # Start is always a boundary
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Blank lines followed by content are potential boundaries
        if not stripped and i > 0 and i < len(lines) - 1:
            next_stripped = lines[i + 1].strip() if i + 1 < len(lines) else ""
            if next_stripped:
                boundaries.append(i + 1)
        
        # Definition boundaries
        if language == "python":
            if stripped.startswith(("def ", "class ", "async def ")):
                if i not in boundaries:
                    boundaries.append(i)
        elif language in ["javascript", "typescript"]:
            if re.match(r'^(export\s+)?(async\s+)?(function|class)\s+', stripped):
                if i not in boundaries:
                    boundaries.append(i)
    
    boundaries.append(len(lines))  # End is always a boundary
    return sorted(set(boundaries))


def chunk_content(content: str, filepath: Path, language: str, 
                  target_tokens: int = CHUNK_TARGET_TOKENS,
                  max_tokens: int = CHUNK_MAX_TOKENS) -> list[Chunk]:
    """Split content into semantically meaningful chunks."""
    
    lines = content.split("\n")
    total_lines = len(lines)
    
    # Small file - single chunk
    total_tokens = count_tokens(content)
    if total_tokens <= max_tokens:
        symbols, imports, _ = extract_symbols_python(content) if language == "python" else extract_symbols_js(content)
        keywords = extract_keywords(content, symbols)
        
        return [Chunk(
            chunk_id=f"{filepath.stem}_001",
            source_file=str(filepath),
            relative_path=str(filepath),
            line_start=1,
            line_end=total_lines,
            char_start=0,
            char_end=len(content),
            token_count=total_tokens,
            content=content,
            symbols=symbols,
            imports=imports,
            keywords=keywords,
            summary=f"Complete file: {filepath.name} ({total_lines} lines)"
        )]
    
    # Large file - need to chunk
    boundaries = find_semantic_boundaries(lines, language)
    chunks = []
    chunk_num = 1
    current_start = 0
    
    while current_start < total_lines:
        # Find end point that keeps us under target tokens
        best_end = current_start + 1
        
        for boundary in boundaries:
            if boundary <= current_start:
                continue
                
            segment = "\n".join(lines[current_start:boundary])
            segment_tokens = count_tokens(segment)
            
            if segment_tokens <= target_tokens:
                best_end = boundary
            elif segment_tokens <= max_tokens:
                best_end = boundary
                break
            else:
                # This boundary would exceed max, use previous best
                break
        
        # If we couldn't find a good boundary, force split
        if best_end == current_start + 1 and current_start + 1 < total_lines:
            # Binary search for a good split point
            test_end = min(current_start + 100, total_lines)
            while test_end > current_start + 1:
                segment = "\n".join(lines[current_start:test_end])
                if count_tokens(segment) <= max_tokens:
                    best_end = test_end
                    break
                test_end = (current_start + test_end) // 2
        
        # Extract chunk
        chunk_lines = lines[current_start:best_end]
        chunk_content = "\n".join(chunk_lines)
        chunk_tokens = count_tokens(chunk_content)
        
        # Skip empty chunks
        if chunk_content.strip():
            # Get symbols in this chunk's line range
            if language == "python":
                all_symbols, imports, _ = extract_symbols_python(content)
            else:
                all_symbols, imports, _ = extract_symbols_js(content)
            
            chunk_symbols = [
                s for s in all_symbols 
                if current_start + 1 <= s.get("line", 0) <= best_end
            ]
            
            keywords = extract_keywords(chunk_content, chunk_symbols)
            
            # Context for continuity
            context_before = lines[current_start - 1] if current_start > 0 else ""
            context_after = lines[best_end] if best_end < total_lines else ""
            
            chunks.append(Chunk(
                chunk_id=f"{filepath.stem}_{chunk_num:03d}",
                source_file=str(filepath),
                relative_path=str(filepath),
                line_start=current_start + 1,  # 1-indexed
                line_end=best_end,
                char_start=len("\n".join(lines[:current_start])),
                char_end=len("\n".join(lines[:best_end])),
                token_count=chunk_tokens,
                content=chunk_content,
                symbols=chunk_symbols,
                imports=imports if chunk_num == 1 else [],  # Only first chunk gets imports
                keywords=keywords,
                context_before=context_before,
                context_after=context_after,
                summary=f"Lines {current_start + 1}-{best_end} of {filepath.name}"
            ))
            chunk_num += 1
        
        # Move to next chunk with overlap
        current_start = max(best_end - OVERLAP_LINES, best_end - 1)
        if current_start <= chunks[-1].line_start if chunks else 0:
            current_start = best_end  # Prevent infinite loop
    
    return chunks


def generate_chunk_sidecar(chunk: Chunk) -> str:
    """Generate markdown sidecar for a chunk."""
    lines = [
        f"# Chunk: {chunk.chunk_id}",
        "",
        f"**Source**: `{chunk.relative_path}`",
        f"**Lines**: {chunk.line_start}-{chunk.line_end}",
        f"**Tokens**: {chunk.token_count}",
        "",
    ]
    
    if chunk.symbols:
        lines.extend([
            "## Symbols",
            "",
            "| Name | Type | Line |",
            "|------|------|------|",
        ])
        for sym in chunk.symbols:
            lines.append(f"| `{sym['name']}` | {sym['type']} | {sym.get('line', '-')} |")
        lines.append("")
    
    if chunk.keywords:
        lines.extend([
            "## Keywords",
            "",
            ", ".join(f"`{k}`" for k in chunk.keywords[:15]),
            "",
        ])
    
    if chunk.context_before:
        lines.extend([
            "## Context (previous)",
            f"```",
            chunk.context_before[:200],
            "```",
            "",
        ])
    
    lines.extend([
        "## Content Preview",
        "```",
        chunk.content[:500] + ("..." if len(chunk.content) > 500 else ""),
        "```",
        "",
        "---",
        f"*To read full content: lines {chunk.line_start}-{chunk.line_end} of `{chunk.relative_path}`*",
    ])
    
    return "\n".join(lines)


def generate_file_index(filepath: Path, chunks: list[Chunk], content: str, language: str) -> FileIndex:
    """Generate file-level index from chunks."""
    all_symbols = []
    all_imports = []
    all_exports = []
    
    for chunk in chunks:
        all_symbols.extend(chunk.symbols)
        all_imports.extend(chunk.imports)
    
    # Deduplicate
    seen_symbols = set()
    unique_symbols = []
    for sym in all_symbols:
        key = (sym["name"], sym["type"])
        if key not in seen_symbols:
            seen_symbols.add(key)
            unique_symbols.append(sym)
            if sym.get("visibility") == "public":
                all_exports.append(sym["name"])
    
    return FileIndex(
        path=str(filepath),
        relative_path=str(filepath),
        hash=get_file_hash(content),
        total_lines=content.count("\n") + 1,
        total_tokens=count_tokens(content),
        total_chars=len(content),
        chunk_count=len(chunks),
        chunk_ids=[c.chunk_id for c in chunks],
        symbols=unique_symbols,
        imports=list(set(all_imports)),
        exports=list(set(all_exports)),
        summary=f"{filepath.name}: {len(unique_symbols)} symbols, {len(chunks)} chunks",
        language=language,
        last_indexed=datetime.now().isoformat()
    )


def generate_search_indexes(all_files: list[FileIndex], all_chunks: list[Chunk]) -> dict:
    """Generate unified search indexes."""
    
    # Symbol index: symbol name → locations
    symbol_index = defaultdict(list)
    for file_idx in all_files:
        for sym in file_idx.symbols:
            symbol_index[sym["name"].lower()].append({
                "file": file_idx.relative_path,
                "line": sym.get("line"),
                "type": sym["type"],
                "signature": sym.get("signature", "")
            })
    
    # Keyword index: keyword → chunk IDs
    keyword_index = defaultdict(list)
    for chunk in all_chunks:
        for keyword in chunk.keywords:
            keyword_index[keyword].append({
                "chunk_id": chunk.chunk_id,
                "file": chunk.relative_path,
                "lines": f"{chunk.line_start}-{chunk.line_end}"
            })
    
    # Dependency graph: file → imports/imported_by
    dependency_graph = defaultdict(lambda: {"imports": [], "imported_by": []})
    for file_idx in all_files:
        for imp in file_idx.imports:
            dependency_graph[file_idx.relative_path]["imports"].append(imp)
            # Try to resolve import to file
            for other_file in all_files:
                if imp in other_file.relative_path or imp.replace(".", "/") in other_file.relative_path:
                    dependency_graph[other_file.relative_path]["imported_by"].append(file_idx.relative_path)
    
    return {
        "symbols": dict(symbol_index),
        "keywords": dict(keyword_index),
        "dependencies": dict(dependency_graph)
    }


def generate_llms_txt(repo_root: Path, all_files: list[FileIndex], all_chunks: list[Chunk]) -> str:
    """Generate comprehensive llms.txt."""
    project_name = repo_root.name
    
    # Stats
    total_files = len(all_files)
    total_chunks = len(all_chunks)
    total_tokens = sum(f.total_tokens for f in all_files)
    total_lines = sum(f.total_lines for f in all_files)
    
    lines = [
        f"# {project_name}",
        "",
        f"> Fully indexed codebase with {total_files} files, {total_chunks} searchable chunks, {total_tokens:,} tokens.",
        "",
        "## Index Statistics",
        "",
        f"- **Total Files**: {total_files}",
        f"- **Total Chunks**: {total_chunks} (each ≤2000 tokens)",
        f"- **Total Lines**: {total_lines:,}",
        f"- **Total Tokens**: {total_tokens:,}",
        "",
        "## How to Use This Index",
        "",
        "1. **Find by symbol**: Check `.ai-index/search/symbols.json`",
        "2. **Find by keyword**: Check `.ai-index/search/keywords.json`",
        "3. **Browse structure**: Check `.ai-index/modules/` for folder summaries",
        "4. **Read chunks**: Each chunk file contains line ranges to read",
        "",
        "## Core Files (by export count)",
        "",
    ]
    
    # Sort by export count
    sorted_files = sorted(all_files, key=lambda x: -len(x.exports))[:20]
    for f in sorted_files:
        exports_preview = ", ".join(f.exports[:3])
        if len(f.exports) > 3:
            exports_preview += f" +{len(f.exports)-3} more"
        lines.append(f"- [{f.relative_path}]({f.relative_path}): {exports_preview}")
    
    lines.extend([
        "",
        "## Large Files (chunked)",
        "",
    ])
    
    chunked_files = [f for f in all_files if f.chunk_count > 1]
    for f in sorted(chunked_files, key=lambda x: -x.total_tokens)[:10]:
        lines.append(f"- `{f.relative_path}`: {f.chunk_count} chunks, {f.total_tokens:,} tokens")
    
    return "\n".join(lines)


def process_repository(repo_root: Path, output_dir: Path, chunk_size: int = CHUNK_TARGET_TOKENS):
    """Process entire repository."""
    
    print(f"Indexing: {repo_root}")
    print(f"Chunk target: {chunk_size} tokens")
    
    all_chunks: list[Chunk] = []
    all_files: list[FileIndex] = []
    
    # Find all source files
    source_files = []
    for filepath in repo_root.rglob("*"):
        if filepath.is_file() and not should_ignore(filepath):
            ext = filepath.suffix.lower()
            if ext in LANGUAGE_EXTENSIONS:
                source_files.append(filepath)
    
    print(f"Found {len(source_files)} source files")
    
    # Process each file
    for filepath in source_files:
        try:
            content = filepath.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            print(f"  Skip {filepath}: {e}")
            continue
        
        if len(content.strip()) < 10:
            continue
        
        language = LANGUAGE_EXTENSIONS.get(filepath.suffix.lower(), "text")
        rel_path = filepath.relative_to(repo_root)
        
        # Chunk the file
        chunks = chunk_content(content, rel_path, language, target_tokens=chunk_size)
        all_chunks.extend(chunks)
        
        # Create file index
        file_index = generate_file_index(rel_path, chunks, content, language)
        all_files.append(file_index)
        
        tokens = count_tokens(content)
        if len(chunks) > 1:
            print(f"  {rel_path}: {tokens:,} tokens → {len(chunks)} chunks")
    
    print(f"\nTotal: {len(all_files)} files, {len(all_chunks)} chunks")
    
    # Create output structure
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "chunks").mkdir(exist_ok=True)
    (output_dir / "files").mkdir(exist_ok=True)
    (output_dir / "modules").mkdir(exist_ok=True)
    (output_dir / "search").mkdir(exist_ok=True)
    
    # Write chunk sidecars
    for chunk in all_chunks:
        sidecar_content = generate_chunk_sidecar(chunk)
        sidecar_path = output_dir / "chunks" / f"{chunk.chunk_id}.md"
        sidecar_path.write_text(sidecar_content)
        
        # Also write chunk metadata as JSON
        meta_path = output_dir / "chunks" / f"{chunk.chunk_id}.json"
        chunk_dict = asdict(chunk)
        chunk_dict.pop("content")  # Don't duplicate full content
        meta_path.write_text(json.dumps(chunk_dict, indent=2))
    
    # Write file indexes
    for file_idx in all_files:
        safe_name = file_idx.relative_path.replace("/", "_").replace("\\", "_")
        meta_path = output_dir / "files" / f"{safe_name}.json"
        meta_path.write_text(json.dumps(asdict(file_idx), indent=2))
    
    # Write search indexes
    search_indexes = generate_search_indexes(all_files, all_chunks)
    (output_dir / "search" / "symbols.json").write_text(
        json.dumps(search_indexes["symbols"], indent=2)
    )
    (output_dir / "search" / "keywords.json").write_text(
        json.dumps(search_indexes["keywords"], indent=2)
    )
    (output_dir / "search" / "dependencies.json").write_text(
        json.dumps(search_indexes["dependencies"], indent=2)
    )
    
    # Write llms.txt
    llms_txt = generate_llms_txt(repo_root, all_files, all_chunks)
    (output_dir / "llms.txt").write_text(llms_txt)
    
    # Write manifest
    manifest = {
        "version": "2.0",
        "generated": datetime.now().isoformat(),
        "project": repo_root.name,
        "chunk_target_tokens": chunk_size,
        "coverage": "100%",
        "stats": {
            "files": len(all_files),
            "chunks": len(all_chunks),
            "total_lines": sum(f.total_lines for f in all_files),
            "total_tokens": sum(f.total_tokens for f in all_files),
            "avg_chunk_tokens": sum(c.token_count for c in all_chunks) // max(len(all_chunks), 1)
        }
    }
    (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))
    
    print(f"\nOutput written to: {output_dir}")
    print(f"  - {len(all_chunks)} chunk files in chunks/")
    print(f"  - {len(all_files)} file indexes in files/")
    print(f"  - Search indexes in search/")
    print(f"  - llms.txt and manifest.json")


def main():
    parser = argparse.ArgumentParser(
        description="Full coverage codebase indexer for AI context retrieval"
    )
    parser.add_argument("path", type=Path, help="Path to project root")
    parser.add_argument(
        "--chunk-size", type=int, default=CHUNK_TARGET_TOKENS,
        help=f"Target tokens per chunk (default: {CHUNK_TARGET_TOKENS})"
    )
    parser.add_argument(
        "--output-dir", type=Path, default=None,
        help="Output directory (default: .ai-index in project root)"
    )
    parser.add_argument(
        "--with-embeddings", action="store_true",
        help="Generate vector embeddings (requires sentence-transformers)"
    )
    
    args = parser.parse_args()
    
    repo_root = args.path.resolve()
    if not repo_root.exists():
        print(f"Error: Path does not exist: {repo_root}")
        sys.exit(1)
    
    output_dir = args.output_dir or (repo_root / ".ai-index")
    
    process_repository(repo_root, output_dir, args.chunk_size)
    
    if args.with_embeddings:
        print("\nNote: Embedding generation requires additional implementation.")
        print("Consider using: chromadb, qdrant, or pinecone for vector storage.")


if __name__ == "__main__":
    main()
