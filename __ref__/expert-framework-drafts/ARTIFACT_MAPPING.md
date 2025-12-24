# Artifact Mapping - Scaffold Deployment Kit

This document maps drafted tmp artifacts to their canonical destinations in the scaffolded OS.

## Promote to Root (Canonical Docs)

- `raw-output/FRAMEWORK.md` → `FRAMEWORK.md`
- `raw-output/FRAMEWORK-CHECKLIST.md` → `FRAMEWORK-CHECKLIST.md`
- `raw-chat-distilled-to-handoff-draft/agentic_contract.txt` → `AGENTIC_WORKFLOW_CONTRACT.md`

## Move to `directives/templates/` (Reference Templates)

These are prompt/workflow templates, not runtime directives:

- `plan.md` → `directives/templates/plan.md`
- `build.md` → `directives/templates/build.md`
- `self-improve.md` → `directives/templates/self-improve.md`
- `plan_build_improve.md` → `directives/templates/plan_build_improve.md`
- `expertise.yaml.example` → `directives/templates/expertise.yaml.example`

## Move to `marked-for-deletion/` (Provenance Only)

These are analysis/planning docs, not runtime OS components:

- `GAP_ANALYSIS.md` → `marked-for-deletion/GAP_ANALYSIS.md`
- `VERIFICATION.md` → `marked-for-deletion/VERIFICATION.md`
- `SUMMARY.md` → `marked-for-deletion/SUMMARY.md`
- `CONTEXT_ENGINEERING_UPDATE.md` → `marked-for-deletion/CONTEXT_ENGINEERING_UPDATE.md`
- `CONTEXT_RESEARCH_PLAN.md` → `marked-for-deletion/CONTEXT_RESEARCH_PLAN.md`
- `INDEX.md` → `marked-for-deletion/INDEX.md`
- `DIRECTORY_STRUCTURE.md` → `marked-for-deletion/DIRECTORY_STRUCTURE.md`
- `AGENTS.example.md` → `marked-for-deletion/AGENTS.example.md`
- `README.md` (long reverse-engineered) → `marked-for-deletion/README_reverse_engineered.md`
- `PRODUCTION_ROADMAP.md` → `marked-for-deletion/PRODUCTION_ROADMAP.md`

## Keep in `__ref/` (Reference Material)

- `__ref/COMPREHENSIVE-KNOWLEDGE-INDEX.md` (stays as reference)
- `__ref/FRAMEWORK-CHECKLIST.md` (stays as reference)
- `__ref/FRAMEWORK.md` (stays as reference)
- All `__ref/PHASE-2-SYNTHESIS-*.md` files (stay as reference)

