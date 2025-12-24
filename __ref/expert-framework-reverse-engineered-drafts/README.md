# Expert Framework - File-Based Agentic Workflow OS

**Project Root**: This directory  
**Status**: ✅ Scaffold Complete

## File Organization

This directory contains:
- **OS Structure** (root) - The scaffolded file-based agentic workflow OS
- **Original Repository Files** (`original-repo/`) - Original drafted files used as reference
- **Temporary Documentation** (`marked-for-deletion/`) - Deployment status and verification files

## Quick Start

```bash
# Navigate to project root
cd /Volumes/uss/cloudworkspace/0_operator/1_Inbox/taskholder/th_agent-EXPERT-framework/__ref/expert-framework-reverse-engineered-drafts

# Validate structure
python scripts/validate_scaffold.py

# Re-scaffold if needed
python scripts/scaffold_os.py --apply --force
```

## Structure

All files are under this root directory:

- `src/agentic_os/` - Core library
- `scripts/` - Deployment scripts
- `directives/` - Behavior contracts
- `executions/` - Python tools
- `shared-knowledgebase/` - Cross-agent knowledge
- `agents/` - 7 agent definitions
- `sessions/`, `eval/`, `test/`, `logs/`, `planning/` - Supporting directories

## Documentation

- `FRAMEWORK.md` - Complete system specification
- `FRAMEWORK-CHECKLIST.md` - Deployment checklist
- `AGENTIC_WORKFLOW_CONTRACT.md` - System contract
- `AGENTS.md` - Agent catalog

## Next Steps

1. Configure agent `.env.example` files with API keys
2. Customize agent system instructions
3. Add knowledge to `shared-knowledgebase/`
4. Create tools in `executions/`

## Additional Resources

- Temporary documentation: `marked-for-deletion/` (deployment status files)
- Original files: `original-repo/` (reference files used for reverse-engineering)

