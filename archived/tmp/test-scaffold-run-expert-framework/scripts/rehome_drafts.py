#!/usr/bin/env python3
"""
Rehome drafted tmp artifacts to their canonical destinations.

Moves files according to ARTIFACT_MAPPING.md:
- Root docs: promote to root
- Templates: move to directives/templates/
- Provenance: move to marked-for-deletion/
"""

import argparse
import shutil
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Rehome drafted artifacts to canonical locations"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview moves without executing"
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually move files (default: dry-run)"
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path.cwd(),
        help="Project root directory"
    )
    
    args = parser.parse_args()
    dry_run = not args.apply
    
    project_root = Path(args.project_root).resolve()
    
    # Source locations
    tmp_dir = project_root / "__ref" / "expert-framework-reverse-engineered-drafts" / "tmp" / "reverse-engineer-expert-framework"
    raw_output = project_root / "raw-output"
    raw_chat = project_root / "raw-chat-distilled-to-handoff-draft"
    
    # Destination locations
    directives_templates = project_root / "directives" / "templates"
    marked_deletion = project_root / "marked-for-deletion"
    
    moves = []
    
    # Promote to root
    if (raw_output / "FRAMEWORK.md").exists():
        moves.append((
            raw_output / "FRAMEWORK.md",
            project_root / "FRAMEWORK.md",
            "promote"
        ))
    if (raw_output / "FRAMEWORK-CHECKLIST.md").exists():
        moves.append((
            raw_output / "FRAMEWORK-CHECKLIST.md",
            project_root / "FRAMEWORK-CHECKLIST.md",
            "promote"
        ))
    if (raw_chat / "agentic_contract.txt").exists():
        moves.append((
            raw_chat / "agentic_contract.txt",
            project_root / "AGENTIC_WORKFLOW_CONTRACT.md",
            "promote"
        ))
    
    # Move to directives/templates/
    template_files = [
        "plan.md",
        "build.md",
        "self-improve.md",
        "plan_build_improve.md",
        "expertise.yaml.example",
    ]
    
    for filename in template_files:
        src = tmp_dir / filename
        if src.exists():
            moves.append((
                src,
                directives_templates / filename,
                "template"
            ))
    
    # Move to marked-for-deletion/
    deletion_files = [
        "GAP_ANALYSIS.md",
        "VERIFICATION.md",
        "SUMMARY.md",
        "CONTEXT_ENGINEERING_UPDATE.md",
        "CONTEXT_RESEARCH_PLAN.md",
        "INDEX.md",
        "DIRECTORY_STRUCTURE.md",
        "AGENTS.example.md",
        "PRODUCTION_ROADMAP.md",
    ]
    
    for filename in deletion_files:
        src = tmp_dir / filename
        if src.exists():
            moves.append((
                src,
                marked_deletion / filename,
                "provenance"
            ))
    
    # Special: README.md -> marked-for-deletion/README_reverse_engineered.md
    readme_src = tmp_dir / "README.md"
    if readme_src.exists():
        moves.append((
            readme_src,
            marked_deletion / "README_reverse_engineered.md",
            "provenance"
        ))
    
    # Execute moves
    if dry_run:
        print("=== DRY-RUN MODE: No files will be moved ===\n")
    
    for src, dst, category in moves:
        if not src.exists():
            print(f"⚠️  Source not found: {src}")
            continue
        
        if dry_run:
            print(f"[DRY-RUN] Would {category}: {src.name}")
            print(f"          → {dst}")
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            if dst.exists():
                print(f"⚠️  Destination exists, skipping: {dst}")
            else:
                shutil.copy2(src, dst)
                print(f"✓ Copied: {src.name} → {dst}")
    
    if dry_run:
        print(f"\n=== DRY-RUN COMPLETE ===")
        print(f"Would process {len(moves)} files")
        print("Run with --apply to actually move files")
    else:
        print(f"\n=== REHOME COMPLETE ===")
        print(f"Processed {len(moves)} files")


if __name__ == "__main__":
    main()

