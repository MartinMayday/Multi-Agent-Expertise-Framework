"""
Symbol extractor using tree-sitter for multi-language AST parsing.

Extracts classes, functions, methods, exports, and type definitions.
Falls back to regex-based extraction when tree-sitter is unavailable.
"""

from __future__ import annotations

import ast
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

try:
    import tree_sitter_languages
    TREE_SITTER_AVAILABLE = True
except ImportError:
    TREE_SITTER_AVAILABLE = False
    logger.warning("tree-sitter-languages not available, using fallback extraction")


@dataclass
class Symbol:
    """Extracted symbol from source code."""
    name: str
    kind: str
    signature: str
    line_number: int
    docstring: Optional[str] = None
    
    def __str__(self) -> str:
        if self.kind == "class":
            return f"class {self.name}"
        elif self.kind == "function":
            return f"def {self.name}()"
        elif self.kind == "method":
            return f".{self.name}()"
        elif self.kind == "export":
            return f"export {self.name}"
        elif self.kind == "type":
            return f"type {self.name}"
        return f"{self.kind} {self.name}"


@dataclass
class FileSymbols:
    """Symbols extracted from a file."""
    path: Path
    language: str
    symbols: list[Symbol] = field(default_factory=list)
    imports: list[str] = field(default_factory=list)
    first_docstring: Optional[str] = None
    
    @property
    def summary(self) -> str:
        """One-line summary of key symbols."""
        parts = []
        classes = [s for s in self.symbols if s.kind == "class"]
        functions = [s for s in self.symbols if s.kind in ("function", "export")]
        
        if classes:
            parts.append(f"class {classes[0].name}")
            if len(classes) > 1:
                parts.append(f"+{len(classes)-1} classes")
        
        if functions:
            parts.append(f"def {functions[0].name}()")
            if len(functions) > 1:
                parts.append(f"+{len(functions)-1} funcs")
        
        return ", ".join(parts) if parts else "no public symbols"


class SymbolExtractor:
    """Multi-language symbol extractor."""
    
    LANGUAGE_MAP = {
        "python": "python",
        "javascript": "javascript",
        "typescript": "typescript",
        "go": "go",
        "rust": "rust",
        "java": "java",
        "c": "c",
        "cpp": "cpp",
        "ruby": "ruby",
        "php": "php",
    }
    
    def __init__(self, use_tree_sitter: bool = True):
        self.use_tree_sitter = use_tree_sitter and TREE_SITTER_AVAILABLE
    
    def extract(self, path: Path, language: str) -> FileSymbols:
        """Extract symbols from a source file."""
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            logger.warning(f"Cannot read {path}: {e}")
            return FileSymbols(path=path, language=language)
        
        if language == "python":
            return self._extract_python_ast(path, content)
        elif self.use_tree_sitter and language in self.LANGUAGE_MAP:
            return self._extract_tree_sitter(path, content, language)
        else:
            return self._extract_regex(path, content, language)
    
    def _extract_python_ast(self, path: Path, content: str) -> FileSymbols:
        """Extract Python symbols using the ast module."""
        result = FileSymbols(path=path, language="python")
        
        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            logger.warning(f"Python parse error in {path}: {e}")
            return self._extract_regex(path, content, "python")
        
        result.first_docstring = ast.get_docstring(tree)
        
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    result.imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    result.imports.append(node.module)
            elif isinstance(node, ast.ClassDef):
                bases = ", ".join(self._get_name(b) for b in node.bases)
                sig = f"class {node.name}({bases})" if bases else f"class {node.name}"
                result.symbols.append(Symbol(
                    name=node.name,
                    kind="class",
                    signature=sig,
                    line_number=node.lineno,
                    docstring=ast.get_docstring(node)
                ))
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        args = self._get_function_args(item)
                        result.symbols.append(Symbol(
                            name=f"{node.name}.{item.name}",
                            kind="method",
                            signature=f"def {item.name}({args})",
                            line_number=item.lineno,
                            docstring=ast.get_docstring(item)
                        ))
            elif isinstance(node, ast.FunctionDef):
                args = self._get_function_args(node)
                result.symbols.append(Symbol(
                    name=node.name,
                    kind="function",
                    signature=f"def {node.name}({args})",
                    line_number=node.lineno,
                    docstring=ast.get_docstring(node)
                ))
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id.isupper():
                        result.symbols.append(Symbol(
                            name=target.id,
                            kind="constant",
                            signature=f"{target.id} = ...",
                            line_number=node.lineno
                        ))
        
        return result
    
    def _get_name(self, node: ast.expr) -> str:
        """Get name from AST node."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        return "..."
    
    def _get_function_args(self, node: ast.FunctionDef) -> str:
        """Get simplified function arguments."""
        args = []
        for arg in node.args.args[:5]:
            args.append(arg.arg)
        if len(node.args.args) > 5:
            args.append("...")
        return ", ".join(args)
    
    def _extract_tree_sitter(self, path: Path, content: str, language: str) -> FileSymbols:
        """Extract symbols using tree-sitter."""
        result = FileSymbols(path=path, language=language)
        
        ts_lang = self.LANGUAGE_MAP.get(language)
        if not ts_lang:
            return self._extract_regex(path, content, language)
        
        try:
            parser = tree_sitter_languages.get_parser(ts_lang)
            tree = parser.parse(content.encode())
        except Exception as e:
            logger.warning(f"tree-sitter parse failed for {path}: {e}")
            return self._extract_regex(path, content, language)
        
        queries = self._get_queries_for_language(ts_lang)
        
        def visit(node):
            node_type = node.type
            
            if node_type in queries.get("class", []):
                name = self._find_child_text(node, "name", content)
                if name:
                    result.symbols.append(Symbol(
                        name=name,
                        kind="class",
                        signature=f"class {name}",
                        line_number=node.start_point[0] + 1
                    ))
            
            elif node_type in queries.get("function", []):
                name = self._find_child_text(node, "name", content)
                if name and not name.startswith("_"):
                    result.symbols.append(Symbol(
                        name=name,
                        kind="function",
                        signature=f"function {name}()",
                        line_number=node.start_point[0] + 1
                    ))
            
            elif node_type in queries.get("import", []):
                text = content[node.start_byte:node.end_byte]
                result.imports.append(text[:100])
            
            for child in node.children:
                visit(child)
        
        visit(tree.root_node)
        return result
    
    def _find_child_text(self, node, child_type: str, content: str) -> Optional[str]:
        """Find text of named child node."""
        for child in node.children:
            if child.type == child_type or child.type == "identifier":
                return content[child.start_byte:child.end_byte]
        return None
    
    def _get_queries_for_language(self, lang: str) -> dict[str, list[str]]:
        """Get node type queries for a language."""
        queries = {
            "javascript": {
                "class": ["class_declaration"],
                "function": ["function_declaration", "arrow_function", "method_definition"],
                "import": ["import_statement"],
            },
            "typescript": {
                "class": ["class_declaration"],
                "function": ["function_declaration", "arrow_function", "method_definition"],
                "import": ["import_statement"],
            },
            "go": {
                "function": ["function_declaration", "method_declaration"],
                "import": ["import_declaration"],
            },
            "rust": {
                "function": ["function_item"],
                "import": ["use_declaration"],
            },
            "java": {
                "class": ["class_declaration"],
                "function": ["method_declaration"],
                "import": ["import_declaration"],
            },
        }
        return queries.get(lang, {})
    
    def _extract_regex(self, path: Path, content: str, language: str) -> FileSymbols:
        """Fallback regex-based extraction."""
        result = FileSymbols(path=path, language=language)
        lines = content.split("\n")
        
        patterns = {
            "python": {
                "class": r"^class\s+(\w+)",
                "function": r"^def\s+(\w+)",
                "import": r"^(?:from|import)\s+([\w.]+)",
            },
            "javascript": {
                "class": r"^(?:export\s+)?class\s+(\w+)",
                "function": r"^(?:export\s+)?(?:async\s+)?function\s+(\w+)",
                "export": r"^export\s+(?:const|let|var|function|class)\s+(\w+)",
            },
            "typescript": {
                "class": r"^(?:export\s+)?class\s+(\w+)",
                "function": r"^(?:export\s+)?(?:async\s+)?function\s+(\w+)",
                "type": r"^(?:export\s+)?(?:type|interface)\s+(\w+)",
            },
        }
        
        lang_patterns = patterns.get(language, patterns.get("javascript", {}))
        
        for i, line in enumerate(lines):
            for kind, pattern in lang_patterns.items():
                match = re.match(pattern, line.strip())
                if match:
                    name = match.group(1)
                    if kind == "import":
                        result.imports.append(name)
                    else:
                        result.symbols.append(Symbol(
                            name=name,
                            kind=kind,
                            signature=line.strip()[:80],
                            line_number=i + 1
                        ))
        
        return result
