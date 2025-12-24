# File Organization - Original vs Generated

**Project Root**: `/Volumes/uss/cloudworkspace/0_operator/1_Inbox/taskholder/th_agent-EXPERT-framework/__ref/expert-framework-reverse-engineered-drafts/`

## Structure Overview

This directory now clearly separates:
- **Original repository files** → `original-repo/`
- **Newly generated OS structure** → Root directory

## Original Files (in `original-repo/`)

These are the original drafted files used as reference for reverse-engineering:

### Example Files
- `database-expert.example.md`
- `question.example.md`
- `plan_build_improve.example.md`
- `planner.example.md`
- `question-w-mermaid-diagrams.md`
- `self-improve.example.md`

### Framework Files
- `notes.md` - Conceptual framework notes
- `SKILL.md` - Skill creation template
- `src_agent-expert-framework.md` - Source agent framework
- `start-orchestrator_skill.md` - Orchestrator skill example

### Drafts
- `tmp/reverse-engineer-expert-framework/` - All reverse-engineered draft files

**Purpose**: These files were used as reference to generate the scaffolded OS structure. They are kept for provenance and future reference.

## Newly Generated OS Structure (Root Directory)

The scaffolded file-based agentic workflow OS:

### Core Directories
- `src/agentic_os/` - Core Python library
- `scripts/` - Deployment scripts
- `directives/` - Behavior contracts
- `executions/` - Python tools
- `shared-knowledgebase/` - Cross-agent knowledge
- `agents/` - 7 agent definitions
- `sessions/` - Execution history
- `eval/` - Evaluation results
- `test/` - Tests
- `logs/` - Audit logs
- `planning/` - Planning state machine
- `marked-for-deletion/` - Provenance docs

### Root Documentation (Generated)
- `FRAMEWORK.md` - Complete system specification
- `FRAMEWORK-CHECKLIST.md` - Deployment checklist
- `AGENTIC_WORKFLOW_CONTRACT.md` - System contract
- `AGENTS.md` - Agent catalog
- `README.md` - Quick start guide
- `SCAFFOLD_COMPLETE.md` - Scaffold summary
- `DEPLOYMENT_READY.md` - Deployment status
- `FINAL_STRUCTURE.md` - Structure verification
- `FILE_ORGANIZATION.md` - This file

## Quick Reference

```bash
# View original files
ls original-repo/

# View generated OS structure
ls -d src scripts directives executions agents shared-knowledgebase

# Validate scaffold
python scripts/validate_scaffold.py
```

## Status

✅ Original files separated into `original-repo/`  
✅ Newly generated OS structure in root  
✅ Clear separation maintained

