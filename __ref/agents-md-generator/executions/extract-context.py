#!/usr/bin/env python3
"""
extract-context.py - Extract contextual snippets and keywords from files

Purpose: Extract contextual snippets, keywords, determine tier assignments,
         generate file purposes and use_when statements

Usage:
    python extract-context.py [TARGET_FOLDER_PATH] [ANALYSIS_JSON_FILE]

Exit codes:
    0 = Success
    1 = Error (file not found, extraction failure)
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Any


def extract_first_paragraph(content: str) -> str:
    """Extract first meaningful paragraph for Level 1 snippet."""
    # Remove frontmatter if present
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            content = parts[2]
    
    # Split into paragraphs
    paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
    
    # Find first non-empty paragraph that's not a heading
    for para in paragraphs:
        if para and not para.startswith('#'):
            # Remove markdown formatting
            para = re.sub(r'[#*_`]', '', para)
            para = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', para)  # Remove links
            if len(para) > 20:  # Meaningful length
                # Limit to first sentence or 200 chars
                sentences = para.split('.')
                if sentences:
                    first_sentence = sentences[0].strip()
                    if len(first_sentence) > 200:
                        return first_sentence[:200] + '...'
                    return first_sentence
                return para[:200] + '...' if len(para) > 200 else para
    
    return "Documentation file"


def extract_keywords(content: str, filename: str) -> List[str]:
    """Extract keywords from file content and name."""
    keywords = set()
    
    # Extract from filename
    filename_lower = filename.lower().replace('.md', '').replace('-', ' ').replace('_', ' ')
    for word in filename_lower.split():
        if len(word) > 3:  # Meaningful words only
            keywords.add(word)
    
    # Extract from frontmatter if present
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 2:
            yaml_content = parts[1]
            # Look for keywords field
            for line in yaml_content.split('\n'):
                if 'keywords:' in line.lower() or 'keyword:' in line.lower():
                    # Extract keywords from YAML array
                    keywords_match = re.search(r'\[([^\]]+)\]', line)
                    if keywords_match:
                        keywords_str = keywords_match.group(1)
                        for kw in keywords_str.split(','):
                            keywords.add(kw.strip().strip('"').strip("'"))
    
    # Extract from headings
    headings = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)
    for heading in headings[:5]:  # First 5 headings
        heading_lower = heading.lower()
        # Extract meaningful words
        for word in re.findall(r'\b[a-z]{4,}\b', heading_lower):
            keywords.add(word)
    
    # Extract from first paragraph (common terms)
    first_para = extract_first_paragraph(content)
    first_para_lower = first_para.lower()
    common_terms = ['guide', 'template', 'example', 'framework', 'protocol', 
                    'execution', 'validation', 'checklist', 'summary', 'overview']
    for term in common_terms:
        if term in first_para_lower:
            keywords.add(term)
    
    # Limit to 10 keywords, prioritize longer words
    keywords_list = sorted(keywords, key=lambda x: (-len(x), x))[:10]
    return keywords_list if keywords_list else ['documentation', 'markdown', 'file']


def determine_tier(filename: str, file_type: str, word_count: int) -> int:
    """Determine tier assignment based on file characteristics."""
    filename_lower = filename.lower()
    
    # Tier 1: Essential files (always load first)
    tier1_patterns = ['readme', 'quick', 'start', 'overview', 'summary', 'index']
    if any(pattern in filename_lower for pattern in tier1_patterns):
        return 1
    if file_type in ['readme', 'quick-start', 'overview', 'summary', 'index']:
        return 1
    
    # Tier 3: Reference files (load only when needed)
    tier3_patterns = ['clog', 'log', 'history', 'archive', 'old', 'backup']
    if any(pattern in filename_lower for pattern in tier3_patterns):
        return 3
    if file_type in ['log']:
        return 3
    if word_count > 10000:  # Very large files are reference
        return 3
    
    # Tier 2: Core execution files (default)
    return 2


def generate_file_purpose(filename: str, file_type: str, content: str, frontmatter: Dict) -> str:
    """Generate specific, actionable file purpose statement."""
    # Try to extract from frontmatter first
    if 'purpose' in frontmatter:
        return frontmatter['purpose']
    if 'description' in frontmatter:
        return frontmatter['description']
    
    # Generate based on file type and content
    first_para = extract_first_paragraph(content)
    
    if file_type == 'readme':
        return f"Overview and quick start guide for the entire package - explains what the package does, how to use it, and where to start"
    elif file_type == 'quick-start':
        return f"Step-by-step execution guide with copy-paste ready prompts and troubleshooting guidance"
    elif file_type == 'template':
        return f"Template file with placeholders for generating new files - provides structure and format"
    elif file_type == 'guide':
        return f"Detailed guide explaining {first_para[:100]}"
    elif file_type == 'sop':
        return f"Standard Operating Procedure with step-by-step instructions and quality gates"
    elif file_type == 'example':
        return f"Example file showing correct implementation and usage patterns"
    elif file_type == 'log':
        return f"Conversation log or historical record documenting generation process or development history"
    else:
        # Generic but specific purpose
        return f"{file_type.replace('-', ' ').title()} file: {first_para[:150]}"


def generate_use_when(filename: str, file_type: str, content: str) -> str:
    """Generate scenario-based use_when statement."""
    filename_lower = filename.lower()
    
    if file_type == 'readme' or 'readme' in filename_lower:
        return "First time using the package, need orientation and understanding of package contents"
    elif file_type == 'quick-start' or 'quick' in filename_lower:
        return "Ready to execute, need exact steps and commands, troubleshooting guidance"
    elif file_type == 'template':
        return "Creating new files based on template, need structure and format"
    elif file_type == 'guide':
        return "Need detailed guidance on specific topic, learning the framework"
    elif file_type == 'sop':
        return "Conducting comprehensive process, need full methodology and quality gates"
    elif file_type == 'example':
        return "Need concrete example, learning the framework, validating approach"
    elif file_type == 'log':
        return "Understanding package origins, historical context, generation process"
    elif file_type == 'index':
        return "Need file navigation, usage matrix, or troubleshooting quick reference"
    elif file_type == 'summary':
        return "First time using package, need orientation and quality guarantees"
    else:
        return "Need reference material for specific task or topic"


def extract_key_concepts(content: str, all_files: List[Dict]) -> List[str]:
    """Extract key concepts from folder content."""
    concepts = set()
    
    # Extract from frontmatter
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 2:
            yaml_content = parts[1]
            # Look for key_concepts field
            for line in yaml_content.split('\n'):
                if 'key_concepts:' in line.lower() or 'concept:' in line.lower():
                    # Extract concepts from YAML array
                    concepts_match = re.findall(r'["\']([^"\']+)["\']', line)
                    concepts.update(concepts_match)
    
    # Extract from headings (H1, H2)
    headings = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)
    for heading in headings[:10]:
        if heading and len(heading) > 10:
            concepts.add(heading.strip())
    
    # Common framework concepts
    content_lower = content.lower()
    framework_terms = {
        'progressive context loading': 'progressive context loading',
        'context loading': 'progressive context loading',
        'tier': 'tiered file loading',
        'agent': 'AI agent',
        'llm': 'LLM context management'
    }
    for term, concept in framework_terms.items():
        if term in content_lower:
            concepts.add(concept)
    
    return sorted(list(concepts))[:10]  # Limit to 10 concepts


def extract_context(folder_path: str, analysis_file: str) -> Dict[str, Any]:
    """Extract context from files based on analysis."""
    folder = Path(folder_path)
    
    # Load analysis JSON
    with open(analysis_file, 'r', encoding='utf-8') as f:
        analysis = json.load(f)
    
    files_context = []
    all_content = []
    
    for file_data in analysis['files']:
        filename = file_data['name']
        file_path = folder / filename
        
        if not file_path.exists():
            continue
        
        # Read file content
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            content = ""
        
        all_content.append(content)
        
        # Extract context data
        snippet = extract_first_paragraph(content)
        keywords = extract_keywords(content, filename)
        tier = determine_tier(filename, file_data.get('file_type', 'documentation'), 
                            file_data.get('word_count', 0))
        purpose = generate_file_purpose(filename, file_data.get('file_type', 'documentation'), 
                                        content, file_data.get('frontmatter', {}))
        use_when = generate_use_when(filename, file_data.get('file_type', 'documentation'), content)
        
        files_context.append({
            'name': filename,
            'snippet': snippet,
            'keywords': keywords,
            'tier': tier,
            'purpose': purpose,
            'use_when': use_when,
            'word_count': file_data.get('word_count', 0),
            'file_type': file_data.get('file_type', 'documentation')
        })
    
    # Extract key concepts from all content
    combined_content = '\n\n'.join(all_content)
    key_concepts = extract_key_concepts(combined_content, files_context)
    
    return {
        'folder_path': folder_path,
        'folder_name': analysis.get('folder_name', folder.name),
        'files': files_context,
        'key_concepts': key_concepts,
        'total_files': len(files_context)
    }


def main():
    """Main execution function."""
    import sys
    
    if len(sys.argv) < 3:
        print("Error: Target folder path and analysis JSON file required", file=sys.stderr)
        print("Usage: python extract-context.py [TARGET_FOLDER_PATH] [ANALYSIS_JSON_FILE]", file=sys.stderr)
        sys.exit(1)
    
    folder_path = sys.argv[1]
    analysis_file = sys.argv[2]
    
    try:
        context = extract_context(folder_path, analysis_file)
        
        # Output JSON to file
        folder_name = Path(folder_path).name
        output_file = f"{folder_name}_context.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(context, f, indent=2, ensure_ascii=False)
        
        print(f"Context extraction complete: {output_file}")
        print(f"  Files processed: {context['total_files']}")
        print(f"  Key concepts: {len(context['key_concepts'])}")
        sys.exit(0)
        
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: Context extraction failed: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

