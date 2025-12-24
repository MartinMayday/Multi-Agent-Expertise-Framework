#!/usr/bin/env python3
"""
Validate the .context/ directory structure and required files.

This tool checks that:
- Required core files exist
- Required directories exist
- Core files have valid frontmatter
- Structure follows the contract
"""

import sys
from pathlib import Path
from typing import List, Tuple


REQUIRED_CORE_FILES = [
    "identity.md",
    "preferences.md",
    "workflows.md",
    "relationships.md",
    "triggers.md",
    "projects.md",
    "rules.md",
    "session.md",
    "journal.md",
]

REQUIRED_DIRECTORIES = [
    "core",
    "conversations",
]

REQUIRED_ROOT_FILES = [
    "README.md",
    "context-update.md",
]


def check_file_exists(filepath: Path) -> Tuple[bool, str]:
    """Check if a file exists and is readable."""
    if not filepath.exists():
        return False, f"Missing: {filepath}"
    if not filepath.is_file():
        return False, f"Not a file: {filepath}"
    if not filepath.stat().st_size > 0:
        return False, f"Empty file: {filepath}"
    return True, ""


def check_directory_exists(dirpath: Path) -> Tuple[bool, str]:
    """Check if a directory exists."""
    if not dirpath.exists():
        return False, f"Missing directory: {dirpath}"
    if not dirpath.is_dir():
        return False, f"Not a directory: {dirpath}"
    return True, ""


def check_frontmatter(filepath: Path) -> Tuple[bool, str]:
    """Check if a markdown file has YAML frontmatter."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        if not content.startswith("---"):
            return False, f"No frontmatter start: {filepath}"
        
        # Check for frontmatter end
        lines = content.split("\n")
        if len(lines) < 2 or lines[1].strip() == "":
            return False, f"Invalid frontmatter: {filepath}"
        
        # Look for closing ---
        found_end = False
        for i, line in enumerate(lines[1:], start=1):
            if line.strip() == "---":
                found_end = True
                break
        
        if not found_end:
            return False, f"No frontmatter end: {filepath}"
        
        return True, ""
    except Exception as e:
        return False, f"Error reading {filepath}: {e}"


def validate_context_tree(project_root: Path) -> Tuple[bool, List[str]]:
    """Validate the .context/ directory structure."""
    context_dir = project_root / ".context"
    errors = []
    
    # Check .context/ exists
    if not context_dir.exists():
        return False, [f"Missing .context/ directory in {project_root}"]
    
    if not context_dir.is_dir():
        return False, [f".context/ is not a directory in {project_root}"]
    
    # Check required root files
    for filename in REQUIRED_ROOT_FILES:
        filepath = context_dir / filename
        exists, msg = check_file_exists(filepath)
        if not exists:
            errors.append(msg)
    
    # Check required directories
    for dirname in REQUIRED_DIRECTORIES:
        dirpath = context_dir / dirname
        exists, msg = check_directory_exists(dirpath)
        if not exists:
            errors.append(msg)
    
    # Check required core files
    core_dir = context_dir / "core"
    if core_dir.exists():
        for filename in REQUIRED_CORE_FILES:
            filepath = core_dir / filename
            exists, msg = check_file_exists(filepath)
            if not exists:
                errors.append(msg)
            else:
                # Check frontmatter for core files
                has_fm, fm_msg = check_frontmatter(filepath)
                if not has_fm:
                    errors.append(fm_msg)
    
    # Check conversations/ has README
    conversations_dir = context_dir / "conversations"
    if conversations_dir.exists():
        readme_path = conversations_dir / "README.md"
        exists, msg = check_file_exists(readme_path)
        if not exists:
            errors.append(msg)
    
    return len(errors) == 0, errors


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        project_root = Path.cwd()
    else:
        project_root = Path(sys.argv[1]).resolve()
    
    if not project_root.exists():
        print(f"Error: Project root does not exist: {project_root}", file=sys.stderr)
        sys.exit(1)
    
    valid, errors = validate_context_tree(project_root)
    
    if valid:
        print("✓ .context/ structure is valid")
        sys.exit(0)
    else:
        print("✗ .context/ structure validation failed:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

