"""
Template rendering utilities for scaffold generation.
"""

from pathlib import Path
from typing import Dict, Any
import re


def render_template(content: str, **kwargs) -> str:
    """
    Simple template rendering using {{PLACEHOLDER}} syntax.
    
    Replaces {{PLACEHOLDER}} with values from kwargs.
    Also supports {{PROJECT_ROOT}} as a special case.
    """
    result = content
    
    # Replace all {{PLACEHOLDER}} patterns
    for key, value in kwargs.items():
        placeholder = f"{{{{{key}}}}}"
        if isinstance(value, Path):
            value = str(value)
        result = result.replace(placeholder, str(value))
    
    # Remove any remaining {{...}} placeholders that weren't replaced
    # (these are intentional placeholders for user to fill)
    # We'll leave them as-is for now
    
    return result


def ensure_directory(path: Path) -> None:
    """Ensure directory exists, creating if needed."""
    path.mkdir(parents=True, exist_ok=True)


def write_file_if_new(path: Path, content: str, force: bool = False) -> bool:
    """
    Write file only if it doesn't exist or force=True.
    
    Returns True if file was written, False if skipped.
    """
    if path.exists() and not force:
        return False
    
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True

