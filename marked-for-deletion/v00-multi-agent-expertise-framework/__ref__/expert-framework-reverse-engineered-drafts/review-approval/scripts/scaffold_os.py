#!/usr/bin/env python3
"""
Scaffold OS Generator - Creates the file-based agentic workflow OS structure.

Usage:
    python scripts/scaffold_os.py [--dry-run] [--apply] [--agents metagpt,researchgpt,...] [--force]
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agentic_os.paths import OSPaths
from agentic_os.render import render_template, ensure_directory, write_file_if_new


def split_core_directives(core_directives_path: Path) -> dict[str, str]:
    """Split core_directives.txt into individual directive files."""
    content = core_directives_path.read_text(encoding="utf-8")
    
    directives = {}
    import re
    
    # Map directive numbers to filenames and checkpoints
    directive_map = {
        1: ("KB_GUARDRAILS.md", "PRE_EXECUTION"),
        2: ("HANDOFF_PROTOCOL.md", "POST_EXECUTION"),
        3: ("PROGRESSIVE_LOADING.md", "CONTEXT_LOADING"),
        4: ("FAILURE_HANDLING.md", "ERROR_DETECTION"),
    }
    
    # Split by "## Directive N:" markers
    pattern = r"## Directive (\d+):\s*([^\n]+)"
    matches = list(re.finditer(pattern, content))
    
    for i, match in enumerate(matches):
        directive_num = int(match.group(1))
        directive_title = match.group(2).strip()
        
        if directive_num not in directive_map:
            continue
        
        filename, checkpoint = directive_map[directive_num]
        
        # Find content from this match to the next match (or end)
        start_pos = match.end()
        end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        
        directive_body = content[start_pos:end_pos].strip()
        
        # Extract frontmatter from the directive header section
        # Look for the markdown code block with frontmatter
        frontmatter_match = re.search(
            r"```markdown\s*\n(---\n.*?\n---)\s*\n```",
            directive_body,
            re.DOTALL
        )
        
        if frontmatter_match:
            # Use the frontmatter from the file
            frontmatter = frontmatter_match.group(1)
            # Remove the entire "### DIRECTIVE HEADER" section including the code block
            directive_body = re.sub(
                r"### DIRECTIVE HEADER\s*\n```markdown\s*\n---\n.*?\n---\s*\n```\s*\n",
                "",
                directive_body,
                flags=re.DOTALL
            )
        else:
            # Generate frontmatter if not found
            directive_id = filename.replace(".md", "")
            frontmatter = f"""---
directive_id: {directive_id}
version: 1.0
enforcement_level: MANDATORY
applies_to: ALL_AGENTS
bypass_allowed: false
validation_checkpoint: {checkpoint}
---"""
        
        # Clean up directive body - remove leading/trailing whitespace
        directive_body = directive_body.strip()
        
        # Remove the "---" separator lines between directives if present
        directive_body = re.sub(r"^---+$", "", directive_body, flags=re.MULTILINE)
        directive_body = directive_body.strip()
        
        # Combine frontmatter and body
        full_content = f"{frontmatter}\n\n{directive_body}\n"
        
        directives[filename] = full_content
    
    return directives


def create_directory_structure(paths: OSPaths, dry_run: bool = False):
    """Create all required OS directories."""
    dirs = [
        paths.directives,
        paths.executions,
        paths.shared_kb,
        paths.agents,
        paths.sessions,
        paths.eval_dir,
        paths.test_dir,
        paths.logs,
        paths.planning,
        paths.scripts,
        paths.src / "agentic_os",  # Ensure src/agentic_os exists
        paths.marked_for_deletion,
        paths.shared_kb / "snippets",
        paths.shared_kb / "frameworks",
        paths.executions / "tools",
        paths.executions / "workflows",
        paths.executions / "utils",
        paths.executions / "eval",
        paths.executions / "hooks",
        paths.logs / "errors",
        paths.sessions / "workflows",
        paths.context,
        paths.context / "core",
        paths.context / "conversations",
    ]
    
    for dir_path in dirs:
        if dry_run:
            print(f"[DRY-RUN] Would create: {dir_path}")
        else:
            ensure_directory(dir_path)
            print(f"Created: {dir_path}")


def create_directives(paths: OSPaths, core_directives_path: Path, dry_run: bool = False, force: bool = False):
    """Create directive files from core_directives.txt."""
    directives = split_core_directives(core_directives_path)
    
    for filename, content in directives.items():
        output_path = paths.directives / filename
        
        # Replace {{PROJECT_ROOT}} placeholder
        content = render_template(content, PROJECT_ROOT=paths.root)
        
        if dry_run:
            print(f"[DRY-RUN] Would write: {output_path} ({len(content)} chars)")
        else:
            if write_file_if_new(output_path, content, force=force):
                print(f"Created: {output_path}")
            else:
                print(f"Skipped (exists): {output_path}")


def create_agent_structure(paths: OSPaths, agent_name: str, dry_run: bool = False, force: bool = False):
    """Create structure for a single agent."""
    agent_dir = paths.agent_dir(agent_name)
    
    # Create agent directories
    subdirs = [
        agent_dir / "test",
        agent_dir / "eval",
        agent_dir / "sessions",
        agent_dir / "directives",
        agent_dir / "executions",
    ]
    
    # Also ensure src/agentic_os exists
    src_dir = paths.src / "agentic_os"
    if not src_dir.exists():
        if dry_run:
            print(f"[DRY-RUN] Would create: {src_dir}")
        else:
            ensure_directory(src_dir)
            print(f"Created: {src_dir}")
    
    for subdir in subdirs:
        if dry_run:
            print(f"[DRY-RUN] Would create: {subdir}")
        else:
            ensure_directory(subdir)
    
    # Agent role descriptions (from contract)
    agent_roles = {
        "metagpt": {
            "role": "Orchestrator - Prompt decomposition and workflow coordination",
            "triggers": "Automatic on braindump prompts",
            "tools": "None (orchestration only)",
        },
        "researchgpt": {
            "role": "Documentation-first research",
            "triggers": "research, find documentation, gather info",
            "tools": "web.search, web.scrape, web.fetch",
        },
        "analysisgpt": {
            "role": "Pattern extraction and synthesis",
            "triggers": "analyze, synthesize, compare",
            "tools": "None (analysis only)",
        },
        "designgpt": {
            "role": "System design and architecture",
            "triggers": "design, architect, plan system",
            "tools": "None (design only)",
        },
        "implementationgpt": {
            "role": "Code generation from specifications",
            "triggers": "implement, build, code",
            "tools": "Write, Read, Bash",
        },
        "testgpt": {
            "role": "Validation and testing",
            "triggers": "test, validate, verify",
            "tools": "Bash, Read",
        },
        "evaluationgpt": {
            "role": "Go/no-go decisions and handoff coordination",
            "triggers": "evaluate, decide, handoff",
            "tools": "Read, Write (reports only)",
        },
    }
    
    role_info = agent_roles.get(agent_name, {
        "role": "Specialized agent",
        "triggers": "TBD",
        "tools": "TBD",
    })
    
    # Create system-instructions.md
    instructions_content = f"""---
name: {agent_name}
description: {role_info['role']}
tools: {role_info['tools']}
model: claude-sonnet-4.5
complexity: intermediate
argument-hint: [task_description]
allowed-tools: {role_info['tools']}
---

# Purpose
{role_info['role']}

## Variables
- TASK: The task description or user request

## Instructions
- READ directives/KB_GUARDRAILS.md and follow strictly
- READ directives/HANDOFF_PROTOCOL.md before any agent transitions
- READ directives/PROGRESSIVE_LOADING.md for context management
- READ directives/FAILURE_HANDLING.md for error handling
- Check kb_{agent_name}-manifest.md before reasoning
- Declare KB sufficiency status (sufficient|partial|insufficient)
- If KB insufficient, halt and ask user for approval to research
- After research, update KB with new findings
- Only then produce task output

## Workflow
1. Check KB manifest (kb_{agent_name}-manifest.md)
2. Declare KB sufficiency
3. If insufficient: request user approval for research
4. If approved: conduct research with source tracking
5. Update KB with findings
6. Execute task
7. Emit handoff contract if transitioning

## Report
Expected output format:
- Task completion status
- KB updates proposed
- Handoff contract (if applicable)
- Source citations

## Examples
USE WHEN: {role_info['triggers']}

Example invocation:
- User: "Research methods for X"
- Agent: [Checks KB] [Declares sufficiency] [Executes research] [Updates KB] [Returns findings]
"""
    
    instructions_path = paths.agent_instructions(agent_name)
    if dry_run:
        print(f"[DRY-RUN] Would write: {instructions_path}")
    else:
        if write_file_if_new(instructions_path, instructions_content, force=force):
            print(f"Created: {instructions_path}")
    
    # Create KB manifest
    kb_manifest_content = f"""---
agent: {agent_name}
kb_type: agent-specific
last_updated: 2025-01-01
total_snippets: 0
---

# {agent_name.title()} Knowledge Manifest

## Quick Reference (Always Loaded)
This agent specializes in: {role_info['role']}

## Knowledge Snippets (Load on Demand)
- No snippets yet. Add knowledge as it accumulates.

## External References
- Global KB: ../shared-knowledgebase/manifest.md
- Related agents: See AGENTS.md
"""
    
    kb_manifest_path = paths.agent_kb_manifest(agent_name)
    if dry_run:
        print(f"[DRY-RUN] Would write: {kb_manifest_path}")
    else:
        if write_file_if_new(kb_manifest_path, kb_manifest_content, force=force):
            print(f"Created: {kb_manifest_path}")
    
    # Create mcp.json template
    mcp_content = """{
  "agent": "{{AGENT_NAME}}",
  "model": "claude-sonnet-4.5",
  "mcp_servers": {
    "web.search": {
      "required": false,
      "priority": "medium",
      "description": "Web search capability"
    }
  }
}
""".replace("{{AGENT_NAME}}", agent_name)
    
    mcp_path = paths.agent_mcp_config(agent_name)
    if dry_run:
        print(f"[DRY-RUN] Would write: {mcp_path}")
    else:
        if write_file_if_new(mcp_path, mcp_content, force=force):
            print(f"Created: {mcp_path}")
    
    # Create .env.example
    env_content = f"""# {agent_name.upper()} Configuration
# Model Selection
AGENT_MODEL=claude-sonnet-4.5
AGENT_FALLBACK_MODEL=claude-haiku-4.5
MODEL_PROVIDER=anthropic

# Multi-Model Options (uncomment to use)
# OPENAI_MODEL=gpt-5.2
# GOOGLE_MODEL=gemini-pro-3.0
# MOONSHOT_MODEL=kimi-k2

# MCP Configuration
MCP_TIMEOUT=30
MCP_RETRY_COUNT=3
"""
    
    env_path = paths.agent_env_example(agent_name)
    if dry_run:
        print(f"[DRY-RUN] Would write: {env_path}")
    else:
        if write_file_if_new(env_path, env_content, force=force):
            print(f"Created: {env_path}")


def create_kb_structure(paths: OSPaths, dry_run: bool = False, force: bool = False):
    """Create KB manifest and framework docs."""
    # KB manifest
    manifest_content = """---
index_type: master-knowledge-catalog
total_snippets: 0
last_updated: 2025-01-01
retrieval_strategy: hybrid (BM25 + semantic + RRF)
---

# Knowledge Base Manifest

## Quick Reference (Always Loaded - L1)
One-line descriptions of knowledge areas will appear here as KB grows.

## Knowledge Categories (L2 - Load on Demand)
### Architecture Patterns
- No patterns yet. Add as discovered.

### Agent Frameworks
- No frameworks yet. Add as discovered.

## Retrieval Optimization
**BM25 Keywords**: [keywords for lexical search]
**Semantic Anchors**: [concepts for embeddings]
**RRF Bridges**: [terminology mappings]
"""
    
    manifest_path = paths.shared_kb / "manifest.md"
    if dry_run:
        print(f"[DRY-RUN] Would write: {manifest_path}")
    else:
        if write_file_if_new(manifest_path, manifest_content, force=force):
            print(f"Created: {manifest_path}")
    
    # KB snippet format doc
    snippet_format_content = """# KB Snippet Format Standard

## Canonical Format

All KB snippets should follow this structure:

```markdown
---
id: unique-snippet-id
title: Snippet Title
source_type: official-doc|partial-doc|conversation-synthesis
source_url: https://example.com/docs
confidence: high|medium|low
tags: [tag1, tag2, tag3]
---

## Summary
Brief summary of the knowledge.

## Verified Facts
- Fact 1
- Fact 2

## Non-Facts / Open Questions
- Unknown 1
- Unknown 2

## Implications
What this means for design/implementation.

## Last Reviewed
YYYY-MM-DD
```

## Why This Format Works
- Frontmatter → retrieval + filtering
- Verified vs Non-Facts → hallucination control
- Implications → design handoff without assumptions
"""
    
    snippet_format_path = paths.shared_kb / "frameworks" / "kb_snippet_format.md"
    if dry_run:
        print(f"[DRY-RUN] Would write: {snippet_format_path}")
    else:
        if write_file_if_new(snippet_format_path, snippet_format_content, force=force):
            print(f"Created: {snippet_format_path}")


def create_context_structure(paths: OSPaths, dry_run: bool = False, force: bool = False):
    """Create .context/ directory structure with minimal skeleton."""
    # Create minimal README
    readme_content = """# Repo Context System (.context/)

This directory contains the repository's persistent memory system.

See `.context/README.md` for full documentation (to be populated after promotion from review-approval/).
"""
    
    readme_path = paths.context / "README.md"
    if dry_run:
        print(f"[DRY-RUN] Would write: {readme_path}")
    else:
        if write_file_if_new(readme_path, readme_content, force=force):
            print(f"Created: {readme_path}")
    
    # Create minimal conversations README
    conversations_readme = """# Conversation Transcripts

This directory contains full conversation transcripts.

See `.context/conversations/README.md` for full documentation (to be populated after promotion from review-approval/).
"""
    
    conversations_readme_path = paths.context / "conversations" / "README.md"
    if dry_run:
        print(f"[DRY-RUN] Would write: {conversations_readme_path}")
    else:
        if write_file_if_new(conversations_readme_path, conversations_readme, force=force):
            print(f"Created: {conversations_readme_path}")
    
    # Note: Core files (identity.md, preferences.md, etc.) will be created from review-approval/.context/ after promotion


def create_root_docs(paths: OSPaths, source_paths: dict, dry_run: bool = False, force: bool = False):
    """Create root documentation files by copying from sources."""
    # Copy FRAMEWORK.md
    if "framework" in source_paths and source_paths["framework"].exists():
        target = paths.root / "FRAMEWORK.md"
        if dry_run:
            print(f"[DRY-RUN] Would copy: {source_paths['framework']} → {target}")
        else:
            if write_file_if_new(target, source_paths["framework"].read_text(encoding="utf-8"), force=force):
                print(f"Created: {target}")
    
    # Copy FRAMEWORK-CHECKLIST.md
    if "checklist" in source_paths and source_paths["checklist"].exists():
        target = paths.root / "FRAMEWORK-CHECKLIST.md"
        if dry_run:
            print(f"[DRY-RUN] Would copy: {source_paths['checklist']} → {target}")
        else:
            if write_file_if_new(target, source_paths["checklist"].read_text(encoding="utf-8"), force=force):
                print(f"Created: {target}")
    
    # Convert agentic_contract.txt to AGENTIC_WORKFLOW_CONTRACT.md
    if "contract" in source_paths and source_paths["contract"].exists():
        target = paths.root / "AGENTIC_WORKFLOW_CONTRACT.md"
        content = source_paths["contract"].read_text(encoding="utf-8")
        # Replace {{PROJECT_ROOT}} placeholder
        content = render_template(content, PROJECT_ROOT=paths.root)
        if dry_run:
            print(f"[DRY-RUN] Would write: {target}")
        else:
            if write_file_if_new(target, content, force=force):
                print(f"Created: {target}")
    
    # Create AGENTS.md catalog
    agents_content = """# Agent Catalog

This catalog lists all available agents in the system. Agents can reference this to discover capabilities and request delegation.

## MetaGPT (Orchestrator)
- **Role**: Prompt decomposition and workflow coordination
- **Invocation**: Automatic on braindump prompts
- **Model**: claude-sonnet-4.5
- **Tools**: None (orchestration only)
- **Location**: agents/metagpt/

## ResearchGPT
- **Role**: Documentation-first research
- **Triggers**: "research", "find documentation", "gather info"
- **Model**: claude-sonnet-4.5
- **Tools**: web.search, web.scrape, web.fetch
- **Location**: agents/researchgpt/

## AnalysisGPT
- **Role**: Pattern extraction and synthesis
- **Triggers**: "analyze", "synthesize", "compare"
- **Model**: claude-sonnet-4.5
- **Tools**: None (analysis only)
- **Location**: agents/analysisgpt/

## DesignGPT
- **Role**: System design and architecture
- **Triggers**: "design", "architect", "plan system"
- **Model**: claude-sonnet-4.5
- **Tools**: None (design only)
- **Location**: agents/designgpt/

## ImplementationGPT
- **Role**: Code generation from specifications
- **Triggers**: "implement", "build", "code"
- **Model**: claude-sonnet-4.5
- **Tools**: Write, Read, Bash
- **Location**: agents/implementationgpt/

## TestGPT
- **Role**: Validation and testing
- **Triggers**: "test", "validate", "verify"
- **Model**: claude-sonnet-4.5
- **Tools**: Bash, Read
- **Location**: agents/testgpt/

## EvaluationGPT
- **Role**: Go/no-go decisions and handoff coordination
- **Triggers**: "evaluate", "decide", "handoff"
- **Model**: claude-sonnet-4.5
- **Tools**: Read, Write (reports only)
- **Location**: agents/evaluationgpt/

## Request New Agent
If no existing agent fits your needs, return to MetaGPT with:
- Required capabilities
- Expected inputs/outputs
- Suggested name
"""
    
    agents_path = paths.root / "AGENTS.md"
    if dry_run:
        print(f"[DRY-RUN] Would write: {agents_path}")
    else:
        if write_file_if_new(agents_path, agents_content, force=force):
            print(f"Created: {agents_path}")


def create_directives_readme(paths: OSPaths, dry_run: bool = False, force: bool = False):
    """Create directives/README.md."""
    readme_content = """# Directives

This directory contains behavior contracts that all agents must follow.

## Core Directives

### KB_GUARDRAILS.md
Mandatory KB-first execution protocol. Prevents agents from producing responses based on assumptions.

### HANDOFF_PROTOCOL.md
Formal state transfer between agents. Ensures work continuity and prevents state loss.

### PROGRESSIVE_LOADING.md
Context management rules. Prevents context window bloat by loading documentation in stages.

### FAILURE_HANDLING.md
Graceful failure handling. Makes failure a first-class outcome with explicit reporting.

## Enforcement

All directives are enforced by MetaGPT at the appropriate checkpoints:
- KB_GUARDRAILS: PRE_EXECUTION
- HANDOFF_PROTOCOL: POST_EXECUTION
- PROGRESSIVE_LOADING: CONTEXT_LOADING
- FAILURE_HANDLING: ERROR_DETECTION

## Usage

Agents must reference applicable directives in their system-instructions.md:

```markdown
## Instructions
- READ directives/KB_GUARDRAILS.md and follow strictly
- READ directives/HANDOFF_PROTOCOL.md before any agent transitions
- ...
```

## Templates

The `templates/` subdirectory contains workflow templates (plan.md, build.md, etc.) that are reference-only, not runtime directives.
"""
    
    readme_path = paths.directives / "README.md"
    if dry_run:
        print(f"[DRY-RUN] Would write: {readme_path}")
    else:
        if write_file_if_new(readme_path, readme_content, force=force):
            print(f"Created: {readme_path}")


def create_agent_hooks_doc(paths: OSPaths, dry_run: bool = False, force: bool = False):
    """Create AGENT_HOOKS.md directive template."""
    hooks_content = """---
directive_id: AGENT_HOOKS
version: 1.0
enforcement_level: OPTIONAL
applies_to: ALL_AGENTS
bypass_allowed: true
validation_checkpoint: POST_EXECUTION
---

# Agent Hooks

## Purpose
Agent hooks provide extension points for custom behavior during agent execution lifecycle.

## Hook Types

### Pre-Execution Hooks
- **When**: Before agent processes task
- **Location**: executions/hooks/pre_execution.py
- **Can**: Modify input, validate prerequisites
- **Cannot**: Skip KB-first checks

### Post-Execution Hooks
- **When**: After agent completes task
- **Location**: executions/hooks/post_execution.py
- **Can**: Update KB, log metrics, trigger notifications
- **Cannot**: Modify agent output

### Error Hooks
- **When**: On agent failure
- **Location**: executions/hooks/on_error.py
- **Can**: Log errors, attempt recovery, notify
- **Cannot**: Suppress errors

## Implementation

Hooks are Python modules that implement standard interfaces:

```python
def pre_execution(agent_name: str, task: dict) -> dict:
    # Modify task if needed
    return task

def post_execution(agent_name: str, result: dict) -> None:
    # Process result
    pass

def on_error(agent_name: str, error: Exception) -> None:
    # Handle error
    pass
```

## Configuration

Hooks are optional. To enable:
1. Create hook module in executions/hooks/
2. Register in agent's mcp.json or system config
3. Ensure hook follows contract (read-only unless explicitly granted write)

## Contract

Hooks must:
- Not modify agent system-instructions.md
- Not bypass directives
- Log all actions
- Fail gracefully if dependencies unavailable
"""
    
    hooks_path = paths.directives / "AGENT_HOOKS.md"
    if dry_run:
        print(f"[DRY-RUN] Would write: {hooks_path}")
    else:
        if write_file_if_new(hooks_path, hooks_content, force=force):
            print(f"Created: {hooks_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Scaffold the file-based agentic workflow OS structure"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without writing files"
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually create files (default: dry-run)"
    )
    parser.add_argument(
        "--agents",
        type=str,
        help="Comma-separated list of agents to scaffold (default: all canonical agents)"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files"
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path.cwd(),
        help="Project root directory (default: current directory)"
    )
    
    args = parser.parse_args()
    
    dry_run = not args.apply
    if dry_run:
        print("=== DRY-RUN MODE: No files will be created ===\n")
    
    paths = OSPaths(args.project_root)
    
    # Determine which agents to scaffold
    if args.agents:
        agent_list = [a.strip() for a in args.agents.split(",")]
    else:
        agent_list = OSPaths.CANONICAL_AGENTS
    
    # Find source files
    project_root = Path(__file__).parent.parent
    source_paths = {
        "framework": project_root / "raw-output" / "FRAMEWORK.md",
        "checklist": project_root / "raw-output" / "FRAMEWORK-CHECKLIST.md",
        "contract": project_root / "raw-chat-distilled-to-handoff-draft" / "agentic_contract.txt",
        "core_directives": project_root / "raw-chat-distilled-to-handoff-draft" / "core_directives.txt",
    }
    
    print("Creating directory structure...")
    create_directory_structure(paths, dry_run=dry_run)
    print()
    
    print("Creating core directives...")
    if source_paths["core_directives"].exists():
        create_directives(paths, source_paths["core_directives"], dry_run=dry_run, force=args.force)
    else:
        print(f"WARNING: {source_paths['core_directives']} not found, skipping directives")
    print()
    
    print("Creating directives README and hooks doc...")
    create_directives_readme(paths, dry_run=dry_run, force=args.force)
    create_agent_hooks_doc(paths, dry_run=dry_run, force=args.force)
    print()
    
    print("Creating KB structure...")
    create_kb_structure(paths, dry_run=dry_run, force=args.force)
    print()
    
    print("Creating .context/ structure...")
    create_context_structure(paths, dry_run=dry_run, force=args.force)
    print()
    
    print(f"Creating {len(agent_list)} agent structures...")
    for agent_name in agent_list:
        create_agent_structure(paths, agent_name, dry_run=dry_run, force=args.force)
    print()
    
    print("Creating root documentation...")
    create_root_docs(paths, source_paths, dry_run=dry_run, force=args.force)
    print()
    
    if dry_run:
        print("\n=== DRY-RUN COMPLETE ===")
        print("Run with --apply to actually create files")
    else:
        print("\n=== SCAFFOLD COMPLETE ===")
        print(f"OS structure created in: {paths.root}")
        print("\nNext steps:")
        print("1. Review generated files")
        print("2. Run: python scripts/validate_scaffold.py")
        print("3. Configure .env files with your API keys")


if __name__ == "__main__":
    main()

