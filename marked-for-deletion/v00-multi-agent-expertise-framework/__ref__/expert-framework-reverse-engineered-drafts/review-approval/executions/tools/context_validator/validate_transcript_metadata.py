#!/usr/bin/env python3
"""
Validate conversation transcript metadata and check for forbidden patterns.

This tool checks that:
- Transcripts have required frontmatter
- No obvious secrets/API keys in transcripts
- Redaction markers are present when needed
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict, Any
import yaml


REQUIRED_FRONTMATTER_FIELDS = [
    "session_id",
    "timestamp",
    "participants",
]

FORBIDDEN_PATTERNS = [
    # API keys (common patterns)
    r'sk-[a-zA-Z0-9]{32,}',
    r'AKIA[0-9A-Z]{16}',
    r'ghp_[a-zA-Z0-9]{36}',
    r'xox[baprs]-[0-9]{11}-[0-9]{11}-[a-zA-Z0-9]{32}',
    # Tokens
    r'Bearer\s+[a-zA-Z0-9\-_]{50,}',
    # Passwords (simple heuristic - long alphanumeric strings)
    r'password["\']?\s*[:=]\s*["\']?[a-zA-Z0-9]{20,}',
    # Private keys
    r'-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----',
]


def extract_frontmatter(filepath: Path) -> Tuple[bool, Dict[str, Any], str]:
    """Extract YAML frontmatter from markdown file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        if not content.startswith("---"):
            return False, {}, "No frontmatter start"
        
        lines = content.split("\n")
        end_idx = None
        for i, line in enumerate(lines[1:], start=1):
            if line.strip() == "---":
                end_idx = i
                break
        
        if end_idx is None:
            return False, {}, "No frontmatter end"
        
        frontmatter_text = "\n".join(lines[1:end_idx])
        try:
            frontmatter = yaml.safe_load(frontmatter_text)
            if frontmatter is None:
                frontmatter = {}
            return True, frontmatter, ""
        except yaml.YAMLError as e:
            return False, {}, f"YAML parse error: {e}"
    except Exception as e:
        return False, {}, f"Error reading file: {e}"


def check_forbidden_patterns(content: str) -> List[Tuple[str, int]]:
    """Check content for forbidden patterns (secrets, API keys, etc.)."""
    violations = []
    lines = content.split("\n")
    
    for line_num, line in enumerate(lines, start=1):
        for pattern in FORBIDDEN_PATTERNS:
            matches = re.finditer(pattern, line, re.IGNORECASE)
            for match in matches:
                # Check if it's in a redaction marker
                if "[REDACTED" not in line:
                    violations.append((pattern, line_num))
    
    return violations


def validate_transcript(filepath: Path) -> Tuple[bool, List[str]]:
    """Validate a single transcript file."""
    errors = []
    
    # Check file exists
    if not filepath.exists():
        return False, [f"File does not exist: {filepath}"]
    
    # Extract frontmatter
    has_fm, frontmatter, fm_error = extract_frontmatter(filepath)
    if not has_fm:
        errors.append(f"Frontmatter error: {fm_error}")
        return False, errors
    
    # Check required fields
    for field in REQUIRED_FRONTMATTER_FIELDS:
        if field not in frontmatter:
            errors.append(f"Missing required field: {field}")
    
    # Check for forbidden patterns
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        violations = check_forbidden_patterns(content)
        if violations:
            for pattern, line_num in violations:
                errors.append(f"Potential secret detected (pattern: {pattern}) at line {line_num}")
    except Exception as e:
        errors.append(f"Error reading content: {e}")
    
    return len(errors) == 0, errors


def validate_all_transcripts(project_root: Path) -> Tuple[bool, List[str]]:
    """Validate all transcripts in .context/conversations/."""
    conversations_dir = project_root / ".context" / "conversations"
    
    if not conversations_dir.exists():
        return True, []  # No transcripts to validate
    
    errors = []
    transcript_files = list(conversations_dir.glob("*.md"))
    
    # Exclude README and template
    transcript_files = [f for f in transcript_files if f.name not in ["README.md", "transcript-template.md"]]
    
    for transcript_file in transcript_files:
        valid, file_errors = validate_transcript(transcript_file)
        if not valid:
            errors.append(f"{transcript_file.name}:")
            errors.extend([f"  - {e}" for e in file_errors])
    
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
    
    valid, errors = validate_all_transcripts(project_root)
    
    if valid:
        print("✓ All transcripts are valid")
        sys.exit(0)
    else:
        print("✗ Transcript validation failed:", file=sys.stderr)
        for error in errors:
            print(f"  {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

