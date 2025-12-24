#!/usr/bin/env python3
"""
analyze-folder.py - Deep analysis of folder structure and files

Purpose: Extract file metadata, structure, relationships, and file types
Output: JSON file with file analysis results

Usage:
    python analyze-folder.py [TARGET_FOLDER_PATH]

Exit codes:
    0 = Success
    1 = Error (folder not found, no markdown files, analysis failure)
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any


def count_words(text: str) -> int:
    """Count words in text (simple whitespace-based count)."""
    return len(text.split())


def extract_frontmatter(content: str) -> Dict[str, Any]:
    """Extract YAML frontmatter from markdown file."""
    frontmatter = {}
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            yaml_content = parts[1].strip()
            # Simple YAML parsing (basic key-value pairs)
            for line in yaml_content.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    frontmatter[key] = value
    return frontmatter


def identify_file_type(filename: str, content: str) -> str:
    """Identify file type based on filename and content."""
    filename_lower = filename.lower()
    
    # Check filename patterns
    if 'readme' in filename_lower:
        return 'readme'
    elif 'quick' in filename_lower and 'start' in filename_lower:
        return 'quick-start'
    elif 'template' in filename_lower:
        return 'template'
    elif 'guide' in filename_lower:
        return 'guide'
    elif 'example' in filename_lower or 'example' in content.lower()[:500]:
        return 'example'
    elif 'sop' in filename_lower:
        return 'sop'
    elif 'clog' in filename_lower or 'log' in filename_lower:
        return 'log'
    elif 'index' in filename_lower:
        return 'index'
    elif 'summary' in filename_lower:
        return 'summary'
    elif 'attachment' in filename_lower:
        return 'attachment'
    else:
        # Check content for clues
        content_lower = content.lower()[:1000]
        if 'overview' in content_lower or 'introduction' in content_lower:
            return 'overview'
        elif 'execution' in content_lower or 'step' in content_lower:
            return 'execution-guide'
        else:
            return 'documentation'


def extract_headings(content: str) -> List[str]:
    """Extract markdown headings from content."""
    headings = []
    for line in content.split('\n'):
        if line.strip().startswith('#'):
            # Remove markdown heading markers
            heading = re.sub(r'^#+\s*', '', line.strip())
            headings.append(heading)
    return headings[:10]  # Limit to first 10 headings


def analyze_file(file_path: Path) -> Dict[str, Any]:
    """Analyze a single markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return {
            'error': f"Cannot read file: {str(e)}",
            'name': file_path.name
        }
    
    # Get file stats
    stat = file_path.stat()
    
    # Extract metadata
    frontmatter = extract_frontmatter(content)
    word_count = count_words(content)
    file_type = identify_file_type(file_path.name, content)
    headings = extract_headings(content)
    
    return {
        'name': file_path.name,
        'path': str(file_path.relative_to(file_path.parent.parent)),
        'size_bytes': stat.st_size,
        'word_count': word_count,
        'last_modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
        'file_type': file_type,
        'has_frontmatter': len(frontmatter) > 0,
        'frontmatter': frontmatter,
        'headings': headings,
        'line_count': len(content.split('\n'))
    }


def analyze_folder(folder_path: str) -> Dict[str, Any]:
    """Analyze folder structure and all markdown files."""
    folder = Path(folder_path)
    
    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path}")
    
    if not folder.is_dir():
        raise ValueError(f"Path is not a directory: {folder_path}")
    
    # Find all markdown files
    markdown_files = list(folder.glob('*.md'))
    
    if not markdown_files:
        raise ValueError(f"No markdown files found in: {folder_path}")
    
    # Analyze each file
    files = []
    for md_file in sorted(markdown_files):
        # Skip AGENTS.md if it already exists (don't analyze output)
        if md_file.name == 'AGENTS.md':
            continue
        file_data = analyze_file(md_file)
        files.append(file_data)
    
    # Calculate folder statistics
    total_words = sum(f.get('word_count', 0) for f in files)
    total_size = sum(f.get('size_bytes', 0) for f in files)
    
    return {
        'folder_path': str(folder.absolute()),
        'folder_name': folder.name,
        'analysis_date': datetime.now().isoformat(),
        'file_count': len(files),
        'total_words': total_words,
        'total_size_bytes': total_size,
        'files': files
    }


def main():
    """Main execution function."""
    import sys
    
    if len(sys.argv) < 2:
        print("Error: Target folder path required", file=sys.stderr)
        print("Usage: python analyze-folder.py [TARGET_FOLDER_PATH]", file=sys.stderr)
        sys.exit(1)
    
    folder_path = sys.argv[1]
    
    try:
        analysis = analyze_folder(folder_path)
        
        # Output JSON to file
        folder_name = Path(folder_path).name
        output_file = f"{folder_name}_analysis.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        
        print(f"Analysis complete: {output_file}")
        print(f"  Files analyzed: {analysis['file_count']}")
        print(f"  Total words: {analysis['total_words']}")
        sys.exit(0)
        
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: Analysis failed: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

