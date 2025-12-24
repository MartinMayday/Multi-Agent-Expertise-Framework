#!/usr/bin/env python3
"""
validate-agents-md.py - Validate generated AGENTS.md file

Purpose: Validate AGENTS.md against all requirements from validation checklist
Output: Validation report with pass/fail status

Usage:
    python validate-agents-md.py [AGENTS_MD_FILE] [TARGET_FOLDER_PATH]

Exit codes:
    0 = All checks passed
    1 = One or more checks failed
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Any

# Try to import yaml, use basic parsing if not available
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


class ValidationResult:
    """Track validation results."""
    def __init__(self):
        self.passed = []
        self.failed = []
        self.warnings = []
    
    def add_pass(self, check: str):
        self.passed.append(check)
    
    def add_fail(self, check: str, details: str = ""):
        self.failed.append((check, details))
    
    def add_warning(self, check: str, details: str = ""):
        self.warnings.append((check, details))
    
    def print_report(self):
        """Print validation report."""
        for check in self.passed:
            print(f"✅ {check}: PASS")
        
        for check, details in self.failed:
            print(f"❌ {check}: FAIL")
            if details:
                print(f"  - {details}")
        
        for check, details in self.warnings:
            print(f"⚠️  {check}: WARNING")
            if details:
                print(f"  - {details}")
        
        total = len(self.passed) + len(self.failed)
        print(f"\nOverall: {'PASS' if not self.failed else 'FAIL'} ({len(self.passed)}/{total} checks passed, {len(self.warnings)} warnings)")


def parse_yaml_frontmatter(content: str) -> Tuple[Dict, str]:
    """Parse YAML frontmatter from markdown file."""
    if not content.startswith('---'):
        return {}, content
    
    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}, content
    
    yaml_content = parts[1].strip()
    markdown_content = parts[2]
    
    try:
        if HAS_YAML:
            frontmatter = yaml.safe_load(yaml_content)
            return frontmatter or {}, markdown_content
        else:
            # Basic YAML parsing (key-value pairs only)
            frontmatter = {}
            for line in yaml_content.split('\n'):
                if ':' in line and not line.strip().startswith('#'):
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    if value.startswith('[') and value.endswith(']'):
                        # Simple array parsing
                        items = [item.strip().strip('"').strip("'") for item in value[1:-1].split(',')]
                        frontmatter[key] = items
                    else:
                        frontmatter[key] = value
            return frontmatter, markdown_content
    except Exception as e:
        raise ValueError(f"YAML parsing error: {e}")


def check_yaml_frontmatter(content: str, result: ValidationResult):
    """Check 1: YAML frontmatter validation."""
    try:
        frontmatter, _ = parse_yaml_frontmatter(content)
        
        # Check required fields
        required_fields = ['title', 'version', 'date', 'status', 'classification']
        for field in required_fields:
            if field not in frontmatter:
                result.add_fail("YAML frontmatter", f"Missing required field: {field}")
                return
        
        # Validate field values
        if not frontmatter.get('title') or not isinstance(frontmatter['title'], str):
            result.add_fail("YAML frontmatter", "Invalid field value: title")
        if not frontmatter.get('version'):
            result.add_fail("YAML frontmatter", "Invalid field value: version")
        
        result.add_pass("YAML frontmatter")
    except ValueError as e:
        result.add_fail("YAML frontmatter", str(e))


def check_required_sections(content: str, result: ValidationResult):
    """Check 2: Required sections validation."""
    # Check CONTEXT section
    if '## CONTEXT' in content or '## 🎯 CONTEXT' in content:
        # Check for all 4 levels
        has_level1 = 'Level 1' in content or 'level 1' in content.lower()
        has_level2 = 'Level 2' in content or 'level 2' in content.lower()
        has_level3 = 'Level 3' in content or 'level 3' in content.lower()
        has_level4 = 'Level 4' in content or 'level 4' in content.lower()
        
        if has_level1 and has_level2 and has_level3 and has_level4:
            result.add_pass("CONTEXT section")
        else:
            missing = []
            if not has_level1: missing.append("Level 1")
            if not has_level2: missing.append("Level 2")
            if not has_level3: missing.append("Level 3")
            if not has_level4: missing.append("Level 4")
            result.add_fail("CONTEXT section", f"Missing levels: {', '.join(missing)}")
    else:
        result.add_fail("CONTEXT section", "CONTEXT section missing")
    
    # Check Document Guide section
    if '## Document Guide' in content or '## 📚 Document Guide' in content:
        result.add_pass("Document Guide section")
    else:
        result.add_fail("Document Guide section", "Document Guide section missing")
    
    # Check file inventory in YAML
    try:
        frontmatter, _ = parse_yaml_frontmatter(content)
        if 'files' in frontmatter and isinstance(frontmatter['files'], list) and len(frontmatter['files']) > 0:
            result.add_pass("File inventory")
        else:
            result.add_fail("File inventory", "File inventory missing or empty")
        
        if 'contextual_snippets' in frontmatter and isinstance(frontmatter['contextual_snippets'], list) and len(frontmatter['contextual_snippets']) > 0:
            result.add_pass("Contextual snippets")
        else:
            result.add_fail("Contextual snippets", "Contextual snippets missing or empty")
    except:
        result.add_fail("File inventory", "Cannot parse file inventory")


def check_tier_assignments(content: str, result: ValidationResult):
    """Check 3: Tier assignment validation."""
    try:
        frontmatter, _ = parse_yaml_frontmatter(content)
        
        # Check contextual_snippets tiers
        if 'contextual_snippets' in frontmatter:
            for snippet in frontmatter['contextual_snippets']:
                tier = snippet.get('tier')
                if tier not in [1, 2, 3]:
                    result.add_fail("Tier assignments", f"Invalid tier: {tier} (must be 1, 2, or 3) in snippet for {snippet.get('file', 'unknown')}")
                    return
        
        # Check files tiers
        if 'files' in frontmatter:
            for file_data in frontmatter['files']:
                tier = file_data.get('tier')
                if tier not in [1, 2, 3]:
                    result.add_fail("Tier assignments", f"Invalid tier: {tier} (must be 1, 2, or 3) for file {file_data.get('name', 'unknown')}")
                    return
        
        result.add_pass("Tier assignments")
    except Exception as e:
        result.add_fail("Tier assignments", f"Error checking tiers: {e}")


def check_placeholders(content: str, result: ValidationResult):
    """Check 4: Placeholder text validation."""
    placeholder_patterns = [
        r'\[PLACEHOLDER\]',
        r'\[FILL_ME\]',
        r'\[REPLACE\]',
        r'\[EXAMPLE\]',
        r'\[CHANGE_ME\]',
        r'\[FOLDER_TITLE\]',
        r'\[FILE_NAME\]',
        r'\[FILE_PURPOSE\]',
        r'\[TIER_ASSIGNMENT\]',
        r'\[KEYWORDS\]',
        r'\[KEY_CONCEPTS\]',
        r'\[OUTCOMES\]'
    ]
    
    found_placeholders = []
    for pattern in placeholder_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            found_placeholders.extend(matches)
    
    if found_placeholders:
        unique_placeholders = list(set(found_placeholders))
        result.add_fail("No placeholders", f"Placeholder text found: {', '.join(unique_placeholders[:5])}")
    else:
        result.add_pass("No placeholders")
    
    # Check for template comments
    template_comment_patterns = [
        r'# REPLACE:',
        r'# EXTRACT:',
        r'# ADD MORE:',
        r'# PLACEHOLDER REPLACEMENT GUIDE'
    ]
    
    found_comments = []
    for pattern in template_comment_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            found_comments.append(pattern)
    
    if found_comments:
        result.add_warning("Template comments", f"Template comments found: {', '.join(found_comments)}")


def check_file_inventory(agents_md_file: str, folder_path: str, result: ValidationResult):
    """Check 5: File inventory validation."""
    try:
        frontmatter, _ = parse_yaml_frontmatter(open(agents_md_file, 'r', encoding='utf-8').read())
        
        if 'files' not in frontmatter:
            result.add_fail("File inventory", "File inventory missing")
            return
        
        # Get actual files in folder
        folder = Path(folder_path)
        actual_files = set(f.name for f in folder.glob('*.md') if f.name != 'AGENTS.md')
        
        # Get files from inventory
        inventory_files = set(f.get('name', '') for f in frontmatter['files'])
        
        # Check completeness
        missing = actual_files - inventory_files
        extra = inventory_files - actual_files
        
        if missing:
            result.add_fail("File inventory", f"Missing files: {', '.join(list(missing)[:5])}")
        elif extra:
            result.add_warning("File inventory", f"Extra files listed: {', '.join(list(extra)[:5])}")
        else:
            result.add_pass("File inventory")
        
        # Check file metadata completeness
        all_complete = True
        for file_data in frontmatter['files']:
            required_fields = ['name', 'purpose', 'use_when', 'tier', 'word_count']
            missing_fields = [f for f in required_fields if f not in file_data]
            if missing_fields:
                result.add_fail("File metadata", f"File {file_data.get('name', 'unknown')} missing fields: {', '.join(missing_fields)}")
                all_complete = False
        
        if all_complete:
            result.add_pass("File metadata")
        
    except Exception as e:
        result.add_fail("File inventory", f"Error checking file inventory: {e}")


def check_key_concepts(content: str, result: ValidationResult):
    """Check 7: Key concepts validation."""
    try:
        frontmatter, _ = parse_yaml_frontmatter(content)
        
        if 'key_concepts' not in frontmatter:
            result.add_fail("Key concepts", "Key concepts missing")
            return
        
        concepts = frontmatter['key_concepts']
        if not isinstance(concepts, list):
            result.add_fail("Key concepts", "Key concepts must be a list")
            return
        
        if len(concepts) < 3:
            result.add_fail("Key concepts", f"Too few concepts: {len(concepts)} (expected: 3-10)")
        elif len(concepts) > 10:
            result.add_warning("Key concepts", f"Too many concepts: {len(concepts)} (expected: 3-10)")
        else:
            result.add_pass("Key concepts")
        
        # Check for generic concepts
        generic_concepts = ['files', 'documentation', 'markdown', 'content']
        generic_found = [c for c in concepts if any(g in str(c).lower() for g in generic_concepts)]
        if generic_found:
            result.add_warning("Key concepts", f"Generic concepts found: {', '.join(generic_found[:3])}")
    
    except Exception as e:
        result.add_fail("Key concepts", f"Error checking key concepts: {e}")


def check_expected_outcomes(content: str, result: ValidationResult):
    """Check 8: Expected outcomes validation."""
    try:
        frontmatter, _ = parse_yaml_frontmatter(content)
        
        if 'outcomes' not in frontmatter:
            result.add_fail("Expected outcomes", "Expected outcomes missing")
            return
        
        outcomes = frontmatter['outcomes']
        if not isinstance(outcomes, list):
            result.add_fail("Expected outcomes", "Expected outcomes must be a list")
            return
        
        if len(outcomes) < 3:
            result.add_fail("Expected outcomes", f"Too few outcomes: {len(outcomes)} (expected: 3-5)")
        elif len(outcomes) > 5:
            result.add_warning("Expected outcomes", f"Too many outcomes: {len(outcomes)} (expected: 3-5)")
        else:
            result.add_pass("Expected outcomes")
    
    except Exception as e:
        result.add_fail("Expected outcomes", f"Error checking expected outcomes: {e}")


def check_content_quality(agents_md_file: str, folder_path: str, result: ValidationResult):
    """Check 9: Content quality validation (snippets, purposes, Document Guide)."""
    try:
        frontmatter, markdown_content = parse_yaml_frontmatter(open(agents_md_file, 'r', encoding='utf-8').read())
        
        # Check 9.1: Snippet content verification
        if 'contextual_snippets' in frontmatter:
            generic_snippet_patterns = ['documentation', 'file', 'content', 'information', 'guide', 'reference']
            for snippet_data in frontmatter['contextual_snippets']:
                snippet_text = str(snippet_data.get('snippet', '')).lower()
                file_name = snippet_data.get('file', 'unknown')
                
                # Check if snippet is too generic
                if any(pattern in snippet_text and len(snippet_text.split()) < 10 for pattern in generic_snippet_patterns):
                    result.add_warning("Snippet content quality", f"Snippet for {file_name} may be too generic (verify by reading actual file)")
        
        # Check 9.2: File purpose specificity
        if 'files' in frontmatter:
            vague_purposes = ['documentation', 'guide', 'file', 'content', 'information', 'reference']
            for file_data in frontmatter['files']:
                purpose = str(file_data.get('purpose', '')).lower()
                file_name = file_data.get('name', 'unknown')
                
                # Check if purpose is too vague
                if any(vague in purpose and len(purpose.split()) < 5 for vague in vague_purposes):
                    result.add_warning("File purpose specificity", f"File purpose for {file_name} may be too vague: '{file_data.get('purpose', '')}' (should be specific and actionable)")
        
        # Check 9.3: Document Guide content verification
        if '## Document Guide' in markdown_content or '## 📚 Document Guide' in markdown_content:
            # Check for generic Document Guide content
            generic_patterns = ['various sections', 'multiple topics', 'different sections', 'various topics']
            for pattern in generic_patterns:
                if pattern in markdown_content.lower():
                    result.add_warning("Document Guide content", f"Document Guide may contain generic content (verify by reading actual files)")
        
        # Check 9.4: Overview text source verification
        overview_section = markdown_content.split('##')[0] if '##' in markdown_content else markdown_content[:500]
        generic_overview = ['collection of files', 'documentation folder', 'set of files', 'group of files']
        if any(pattern in overview_section.lower() for pattern in generic_overview):
            result.add_warning("Overview text source", "Overview text may be generic (verify by reading README)")
        
        # Check 9.5: Key concepts source verification
        if 'key_concepts' in frontmatter:
            generic_concepts = ['files', 'documentation', 'markdown', 'content', 'information']
            for concept in frontmatter['key_concepts']:
                concept_str = str(concept).lower()
                if any(generic in concept_str for generic in generic_concepts):
                    result.add_warning("Key concepts source", f"Key concept may be too generic: '{concept}' (should be specific to folder content)")
        
        # If no warnings, pass
        result.add_pass("Content quality")
    
    except Exception as e:
        result.add_warning("Content quality", f"Error checking content quality: {e} (manual verification recommended)")


def main():
    """Main execution function."""
    import sys
    
    if len(sys.argv) < 3:
        print("Error: AGENTS.md file and target folder path required", file=sys.stderr)
        print("Usage: python validate-agents-md.py [AGENTS_MD_FILE] [TARGET_FOLDER_PATH]", file=sys.stderr)
        sys.exit(1)
    
    agents_md_file = sys.argv[1]
    folder_path = sys.argv[2]
    
    if not os.path.exists(agents_md_file):
        print(f"Error: AGENTS.md file not found: {agents_md_file}", file=sys.stderr)
        sys.exit(1)
    
    if not os.path.exists(folder_path):
        print(f"Error: Target folder not found: {folder_path}", file=sys.stderr)
        sys.exit(1)
    
    try:
        with open(agents_md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        result = ValidationResult()
        
        # Run all validation checks
        check_yaml_frontmatter(content, result)
        check_required_sections(content, result)
        check_tier_assignments(content, result)
        check_placeholders(content, result)
        check_file_inventory(agents_md_file, folder_path, result)
        check_key_concepts(content, result)
        check_expected_outcomes(content, result)
        check_content_quality(agents_md_file, folder_path, result)
        
        # Print report
        result.print_report()
        
        # Exit with appropriate code
        sys.exit(0 if not result.failed else 1)
        
    except Exception as e:
        print(f"Error: Validation failed: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    import sys
    main()

