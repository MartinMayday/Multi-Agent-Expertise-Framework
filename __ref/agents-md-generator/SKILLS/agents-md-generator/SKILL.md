---
name: agents-md-generator
description: Generate AGENTS.md files with progressive context loading for any folder. Analyzes folder contents, extracts context, and creates vendor-neutral context files following AGENTS.md best practices.
version: 1.0.0
author: BMAD Method + 5 Enhancements
---

# AGENTS.md Generator Skill

**Purpose:** Automatically generate production-ready `AGENTS.md` files for any folder with progressive context loading integrated by default.

**Version:** 1.0.0  
**Status:** Production Ready

---

## What This Skill Does

This skill enables tasker-execution-agents to automatically generate `AGENTS.md` files for any target folder. The generated files follow AGENTS.md best practices and include progressive context loading protocol (4 levels) to reduce context bloat by 85%.

**Key Features:**
- Deep file analysis (metadata, structure, relationships)
- Context extraction (snippets, keywords, tier assignments)
- Template-driven generation (consistent format)
- Comprehensive validation (quality gates)
- Progressive context loading (4-level system)

---

## How to Use This Skill

### Quick Start

1. **Identify target folder** that needs AGENTS.md
2. **Load this skill** (Claude will auto-detect)
3. **Provide folder path** to generate AGENTS.md for
4. **Skill executes** 5 phases automatically:
   - Phase 1: Analyze folder
   - Phase 2: Extract context
   - Phase 3: Generate AGENTS.md
   - Phase 4: Validate output
   - Phase 5: Refine if needed

### Example Usage

```
User: "Generate AGENTS.md for __ref/interview-framework folder"

Claude: "I'll generate AGENTS.md for the interview-framework folder using the agents-md-generator skill."
[Executes phases 1-5]
[Outputs: __ref/interview-framework/AGENTS.md]
```

---

## Progressive Context Loading

This skill generates AGENTS.md files with progressive context loading built-in:

**Level 1: Front Matter (Always Loaded)** - ~200 tokens
- Brief description, keywords, key concepts
- AI agent decides if package is relevant

**Level 2: AGENTS.md Content (On-Demand)** - ~2,000 tokens
- Complete file inventory and document guide
- Loads when AI confirms package relevance

**Level 3: Reference Files (Selectively Loaded)** - Variable tokens
- Individual files loaded only when needed
- Tiered by importance (1=essential, 2=core, 3=reference)

**Level 4: Source Code (Execute, Don't Load)** - ~100 tokens output only
- Scripts execute externally
- Only output loaded to context

**Result:** 85% context reduction vs. loading everything upfront

---

## Skill Structure

### Directives (Instructions)
- `MISSION-OBJECTIVES.md` - Mission, success criteria, constraints
- `TASKER-ORDERS.md` - Step-by-step execution instructions
- `AGENTS-MD-TEMPLATE.md` - Template with placeholders
- `EXAMPLES-WRONG-vs-CORRECT.md` - Common mistakes and solutions
- `VALIDATION-CHECKLIST.md` - Quality gates and validation criteria

### Executions (Scripts)
- `analyze-folder.py` - Deep file analysis and metadata extraction
- `extract-context.py` - Contextual snippet and keyword extraction
- `validate-agents-md.py` - Validation of generated AGENTS.md

### References
- Progressive context loading framework
- AGENTS.md best practices
- Validation requirements

---

## Execution Flow

```
1. Analyze Folder
   ↓
2. Extract Context
   ↓
3. Generate AGENTS.md (using template)
   ↓
4. Validate Output
   ↓
5. Refine (if needed)
   ↓
✅ AGENTS.md Ready
```

---

## Output Quality

Generated AGENTS.md files include:
- ✅ Valid YAML frontmatter
- ✅ Complete CONTEXT section (4 levels)
- ✅ Accurate file inventory
- ✅ Logical tier assignments
- ✅ Specific file purposes
- ✅ Scenario-based use_when statements
- ✅ Key concepts extracted from content
- ✅ Expected outcomes derived from purpose
- ✅ No placeholder text
- ✅ Vendor-neutral format

---

## When to Use This Skill

**Use this skill when:**
- You have a folder with multiple markdown files
- You want to create AGENTS.md for progressive context loading
- You need vendor-neutral context files (not CLAUDE.md specific)
- You want consistent AGENTS.md format across folders

**Don't use this skill when:**
- Folder has no markdown files
- You need CLAUDE.md (tool-specific) instead of AGENTS.md
- Folder is empty or contains only non-markdown files

---

## Success Criteria

A generated AGENTS.md is successful when:
- ✅ All validation checks pass
- ✅ CONTEXT section includes all 4 levels
- ✅ File inventory matches actual files
- ✅ Tier assignments are logical
- ✅ No placeholder text remains
- ✅ Ready for use by AI/LLM agents

---

## References

- **Directives:** `directives/MISSION-OBJECTIVES.md`, `directives/TASKER-ORDERS.md`
- **Template:** `directives/AGENTS-MD-TEMPLATE.md`
- **Examples:** `directives/EXAMPLES-WRONG-vs-CORRECT.md`
- **Validation:** `directives/VALIDATION-CHECKLIST.md`
- **Scripts:** `executions/analyze-folder.py`, `executions/extract-context.py`, `executions/validate-agents-md.py`

---

## Progressive Loading for This Skill

**Level 1 (Always Loaded):** This SKILL.md description  
**Level 2 (On-Demand):** Full directives and template  
**Level 3 (Selective):** Specific directive files as needed  
**Level 4 (Execute):** Python scripts execute, output only loaded

---

**Ready to generate AGENTS.md files with progressive context loading.** 🚀

