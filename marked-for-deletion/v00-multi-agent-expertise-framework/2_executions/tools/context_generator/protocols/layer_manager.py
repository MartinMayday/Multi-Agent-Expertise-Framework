"""Layer protocol manager for progressive context loading (L1-L4)."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class LayerOutput:
    """Output for a single layer."""
    layer_num: int
    name: str
    description: str
    content: str
    tokens_estimate: int = 0


@dataclass
class MultiLayerOutput:
    """Complete multi-layer output for a folder."""
    folder_name: str
    folder_path: Path
    purpose: str
    
    layer_1: Optional[LayerOutput] = None  # Quick index
    layer_2: Optional[LayerOutput] = None  # Structured YAML
    layer_3: Optional[LayerOutput] = None  # Rich context
    layer_4: Optional[LayerOutput] = None  # Raw references
    
    all_layers_combined: str = ""
    layer_manifest: dict = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for template rendering."""
        return {
            'folder_name': self.folder_name,
            'folder_path': str(self.folder_path),
            'purpose': self.purpose,
            'layer_1': self.layer_1,
            'layer_2': self.layer_2,
            'layer_3': self.layer_3,
            'layer_4': self.layer_4,
            'all_layers_combined': self.all_layers_combined,
            'layer_manifest': self.layer_manifest,
        }


class LayerProtocolManager:
    """Manages progressive context loading through 4 layers."""
    
    LAYER_DEFINITIONS = {
        1: {
            'name': 'L1: Quick Index',
            'description': 'Fast discovery layer - file names, types, keywords only',
            'purpose': 'Initial folder discovery',
            'format': 'Plain text index',
            'use_case': 'Agent quickly scans available files',
            'typical_tokens': '200-300',
        },
        2: {
            'name': 'L2: Structured Metadata',
            'description': 'Detailed layer - YAML frontmatter with all metadata',
            'purpose': 'Detailed file exploration',
            'format': 'YAML frontmatter blocks',
            'use_case': 'Agent selects relevant files for context',
            'typical_tokens': '800-1200',
        },
        3: {
            'name': 'L3: Rich Context',
            'description': 'Context window layer - summaries, dependencies, relationships',
            'purpose': 'In-depth context understanding',
            'format': 'Markdown with summaries and maps',
            'use_case': 'Agent needs detailed understanding of architecture',
            'typical_tokens': '2000-5000',
        },
        4: {
            'name': 'L4: Raw References',
            'description': 'Reference layer - file paths, content pointers, byte ranges',
            'purpose': 'Complete content retrieval',
            'format': 'File manifest and references',
            'use_case': 'Agent needs to read actual file content',
            'typical_tokens': 'full file content',
        },
    }
    
    def __init__(self):
        """Initialize layer manager."""
        pass
    
    def generate_layer_1(
        self,
        folder_name: str,
        files: list[dict],
        purpose: str = ""
    ) -> LayerOutput:
        """
        Generate L1: Quick Index.
        
        Provides fast discovery through minimal metadata:
        - File names
        - Chunk types
        - Top keywords
        
        Args:
            folder_name: Name of folder
            files: List of file metadata dicts
            purpose: Folder purpose
            
        Returns:
            LayerOutput with index content
        """
        lines = []
        
        lines.append(f"# {folder_name} - Quick Index\n")
        if purpose:
            lines.append(f"**Purpose**: {purpose}\n")
        
        lines.append(f"**Files**: {len(files)} total\n\n")
        
        lines.append("## Files by Type\n")
        
        # Group by chunk type
        by_type = {}
        for f in files:
            chunk_type = f.get('chunk_type', 'unknown')
            if chunk_type not in by_type:
                by_type[chunk_type] = []
            by_type[chunk_type].append(f)
        
        # Generate index
        for chunk_type in sorted(by_type.keys()):
            files_of_type = by_type[chunk_type]
            lines.append(f"\n### {chunk_type.title()} ({len(files_of_type)})\n")
            
            for f in sorted(files_of_type, key=lambda x: x.get('name', '')):
                name = f.get('name', 'unknown')
                keywords = f.get('keywords', [])
                top_keywords = ', '.join(keywords[:3]) if keywords else 'N/A'
                lines.append(f"- **{name}**: {top_keywords}\n")
        
        # Add discovery hints
        lines.append("\n## Quick Navigation\n\n")
        lines.append("- 📋 [L2: Metadata] for detailed file information\n")
        lines.append("- 🏗️ [L3: Context] for architecture and dependencies\n")
        lines.append("- 📄 [L4: References] for raw file content\n")
        
        content = "".join(lines)
        tokens = len(content) // 4  # Rough estimate
        
        return LayerOutput(
            layer_num=1,
            name=self.LAYER_DEFINITIONS[1]['name'],
            description=self.LAYER_DEFINITIONS[1]['description'],
            content=content,
            tokens_estimate=tokens,
        )
    
    def generate_layer_2(
        self,
        folder_name: str,
        files: list[dict],
        purpose: str = ""
    ) -> LayerOutput:
        """
        Generate L2: Structured Metadata.
        
        Provides detailed YAML frontmatter blocks for each file.
        
        Args:
            folder_name: Name of folder
            files: List of file metadata dicts
            purpose: Folder purpose
            
        Returns:
            LayerOutput with YAML frontmatter blocks
        """
        lines = []
        
        lines.append(f"# {folder_name} - File Metadata\n\n")
        
        lines.append("## Layer 2: Structured Metadata\n\n")
        lines.append("Each file includes YAML frontmatter with:\n")
        lines.append("- Unique identifier and relative path\n")
        lines.append("- Classification (contract, methodology, architecture, execution, reference)\n")
        lines.append("- Semantic keywords for search\n")
        lines.append("- Loading conditions (when to load this file)\n")
        lines.append("- Retrieval triggers (semantic phrases for RAG)\n\n")
        
        # Add sorted files
        for f in sorted(files, key=lambda x: x.get('name', '')):
            name = f.get('name', 'unknown')
            lines.append(f"### {name}\n\n")
            
            # Build YAML block
            yaml_lines = ["---"]
            yaml_lines.append(f"id: {f.get('id', 'unknown')}")
            yaml_lines.append(f"path: {f.get('path', 'unknown')}")
            yaml_lines.append(f"tokens: {f.get('tokens', 0)}")
            yaml_lines.append(f"chunk_type: {f.get('chunk_type', 'reference')}")
            
            keywords = f.get('keywords', [])
            if keywords:
                yaml_lines.append(f"keywords:")
                for kw in keywords[:10]:
                    yaml_lines.append(f"  - {kw}")
            
            priority = f.get('priority', 'medium')
            yaml_lines.append(f"priority: {priority}")
            
            when_to_load = f.get('when_to_load', [])
            if when_to_load:
                yaml_lines.append(f"when_to_load:")
                for cond in when_to_load:
                    yaml_lines.append(f"  - {cond}")
            
            triggers = f.get('retrieval_triggers', [])
            if triggers:
                yaml_lines.append(f"retrieval_triggers:")
                for trig in triggers:
                    yaml_lines.append(f"  - {trig}")
            
            yaml_lines.append("---\n")
            
            lines.append("\n".join(yaml_lines))
            lines.append("\n")
        
        content = "".join(lines)
        tokens = len(content) // 4
        
        return LayerOutput(
            layer_num=2,
            name=self.LAYER_DEFINITIONS[2]['name'],
            description=self.LAYER_DEFINITIONS[2]['description'],
            content=content,
            tokens_estimate=tokens,
        )
    
    def generate_layer_3(
        self,
        folder_name: str,
        files: list[dict],
        purpose: str = "",
        dependencies: str = ""
    ) -> LayerOutput:
        """
        Generate L3: Rich Context.
        
        Provides comprehensive context with summaries and relationships.
        
        Args:
            folder_name: Name of folder
            files: List of file metadata dicts
            purpose: Folder purpose
            dependencies: Dependency summary
            
        Returns:
            LayerOutput with rich context
        """
        lines = []
        
        lines.append(f"# {folder_name} - Rich Context\n\n")
        
        if purpose:
            lines.append(f"## Purpose\n{purpose}\n\n")
        
        # Dependency map
        if dependencies:
            lines.append(f"## Architecture & Dependencies\n{dependencies}\n\n")
        
        # Files with summaries
        lines.append("## File Details\n\n")
        
        # Sort by priority and ranking
        sorted_files = sorted(
            files,
            key=lambda x: (
                {'high': 0, 'medium': 1, 'low': 2}.get(x.get('priority', 'medium'), 1),
                -x.get('retrieval_score', 0),
            )
        )
        
        for f in sorted_files:
            name = f.get('name', 'unknown')
            chunk_type = f.get('chunk_type', 'reference')
            tokens = f.get('tokens', 0)
            description = f.get('description', 'No description available')
            ragas = f.get('ragas_score', 0.0)
            
            lines.append(f"### {name}\n\n")
            lines.append(f"- **Type**: {chunk_type.title()}\n")
            lines.append(f"- **Tokens**: ~{tokens}\n")
            lines.append(f"- **Quality**: {ragas:.1%} (RAGAS score)\n")
            lines.append(f"- **Description**: {description}\n\n")
        
        lines.append("## Layer 3 Characteristics\n\n")
        lines.append("This layer provides:\n")
        lines.append("- ✓ Comprehensive file descriptions\n")
        lines.append("- ✓ Dependency relationships\n")
        lines.append("- ✓ Quality metrics (RAGAS scores)\n")
        lines.append("- ✓ Context for deep understanding\n")
        
        content = "".join(lines)
        tokens = len(content) // 4
        
        return LayerOutput(
            layer_num=3,
            name=self.LAYER_DEFINITIONS[3]['name'],
            description=self.LAYER_DEFINITIONS[3]['description'],
            content=content,
            tokens_estimate=tokens,
        )
    
    def generate_layer_4(
        self,
        folder_name: str,
        folder_path: Path,
        files: list[dict]
    ) -> LayerOutput:
        """
        Generate L4: Raw References.
        
        Provides file paths and content pointers for raw retrieval.
        
        Args:
            folder_name: Name of folder
            folder_path: Path to folder
            files: List of file metadata dicts
            
        Returns:
            LayerOutput with file manifest and references
        """
        lines = []
        
        lines.append(f"# {folder_name} - File Manifest\n\n")
        
        lines.append("## File References\n\n")
        
        # File manifest as CSV-like format
        lines.append("| File | Type | Size | ID | Path |\n")
        lines.append("|------|------|------|----|----- |\n")
        
        for f in sorted(files, key=lambda x: x.get('name', '')):
            name = f.get('name', 'unknown')
            chunk_type = f.get('chunk_type', 'reference')
            tokens = f.get('tokens', 0)
            file_id = f.get('id', 'unknown')
            path = f.get('path', 'unknown')
            
            lines.append(f"| {name} | {chunk_type} | ~{tokens} | {file_id} | {path} |\n")
        
        lines.append("\n## Raw Content Locations\n\n")
        lines.append(f"**Folder Path**: `{folder_path}`\n\n")
        
        lines.append("## Usage Instructions\n\n")
        lines.append("L4 provides direct file references for:\n")
        lines.append("1. Reading complete file contents\n")
        lines.append("2. Byte-range retrieval for large files\n")
        lines.append("3. Direct file access by ID or path\n")
        lines.append("4. Raw content integration into LLM context\n\n")
        
        lines.append("## File Retrieval Map\n\n")
        for f in sorted(files, key=lambda x: x.get('name', '')):
            file_id = f.get('id', 'unknown')
            path = f.get('path', 'unknown')
            lines.append(f"- `{file_id}` → {path}\n")
        
        content = "".join(lines)
        tokens = len(content) // 4
        
        return LayerOutput(
            layer_num=4,
            name=self.LAYER_DEFINITIONS[4]['name'],
            description=self.LAYER_DEFINITIONS[4]['description'],
            content=content,
            tokens_estimate=tokens,
        )
    
    def generate_all_layers(
        self,
        folder_name: str,
        folder_path: Path,
        files: list[dict],
        purpose: str = "",
        dependencies: str = ""
    ) -> MultiLayerOutput:
        """
        Generate all 4 layers.
        
        Args:
            folder_name: Name of folder
            folder_path: Path to folder
            files: List of file metadata dicts
            purpose: Folder purpose
            dependencies: Dependency summary
            
        Returns:
            MultiLayerOutput with all layers
        """
        layer_1 = self.generate_layer_1(folder_name, files, purpose)
        layer_2 = self.generate_layer_2(folder_name, files, purpose)
        layer_3 = self.generate_layer_3(folder_name, files, purpose, dependencies)
        layer_4 = self.generate_layer_4(folder_name, folder_path, files)
        
        # Combine all layers
        combined = f"""# {folder_name} - Multi-Layer Context

## Overview

This documentation provides progressive context loading through 4 layers:

- **L1**: Quick Index (discovery)
- **L2**: Structured Metadata (file selection)
- **L3**: Rich Context (understanding)
- **L4**: Raw References (retrieval)

---

## {layer_1.name}

{layer_1.description}

### Tokens: ~{layer_1.tokens_estimate}

{layer_1.content}

---

## {layer_2.name}

{layer_2.description}

### Tokens: ~{layer_2.tokens_estimate}

{layer_2.content}

---

## {layer_3.name}

{layer_3.description}

### Tokens: ~{layer_3.tokens_estimate}

{layer_3.content}

---

## {layer_4.name}

{layer_4.description}

### Tokens: ~{layer_4.tokens_estimate}

{layer_4.content}

---

## Layer Selection Guide

| Need | Layer | Why |
|------|-------|-----|
| Fast file discovery | L1 | Minimal tokens (~250) |
| Detailed file info | L2 | Structured metadata (~1000) |
| Deep understanding | L3 | Summaries + context (~3000) |
| Raw content | L4 | Direct file access (~unlimited) |
"""
        
        # Build manifest
        manifest = {
            'folder': folder_name,
            'purpose': purpose,
            'layer_1': {
                'name': layer_1.name,
                'tokens': layer_1.tokens_estimate,
            },
            'layer_2': {
                'name': layer_2.name,
                'tokens': layer_2.tokens_estimate,
            },
            'layer_3': {
                'name': layer_3.name,
                'tokens': layer_3.tokens_estimate,
            },
            'layer_4': {
                'name': layer_4.name,
                'tokens': layer_4.tokens_estimate,
            },
            'total_tokens': (
                layer_1.tokens_estimate +
                layer_2.tokens_estimate +
                layer_3.tokens_estimate +
                layer_4.tokens_estimate
            ),
        }
        
        return MultiLayerOutput(
            folder_name=folder_name,
            folder_path=folder_path,
            purpose=purpose,
            layer_1=layer_1,
            layer_2=layer_2,
            layer_3=layer_3,
            layer_4=layer_4,
            all_layers_combined=combined,
            layer_manifest=manifest,
        )
