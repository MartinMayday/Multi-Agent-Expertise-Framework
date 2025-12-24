# Quick Start Prompt: AGENTS.md Generator

**Copy/paste this prompt into your terminal or IDE to start generating AGENTS.md files.**

---

## Inline Prompt (Copy/Paste Ready)

```
Generate AGENTS.md for folder=[TARGET_FOLDER_PATH] using SOP at __ref/SOPs/agents-md-generator

CRITICAL: Follow the SOP workflow exactly:

1. PRE-FLIGHT (MANDATORY):
   - Read __ref/SOPs/agents-md-generator/directives/MISSION-OBJECTIVES.md
   - Read __ref/SOPs/agents-md-generator/directives/TASKER-ORDERS.md
   - Read __ref/SOPs/agents-md-generator/directives/AGENTS-MD-TEMPLATE.md
   - Read __ref/SOPs/agents-md-generator/directives/VALIDATION-CHECKLIST.md
   - Verify you understand the 5-phase workflow before proceeding

2. PHASE 1: Analyze Target Folder
   - Execute: python __ref/SOPs/agents-md-generator/executions/analyze-folder.py [TARGET_FOLDER_PATH]
   - Verify: [TARGET_FOLDER]_analysis.json created successfully

3. PHASE 2: Extract Context from Files
   - CRITICAL: Read at least first 500 words of EACH markdown file in target folder
   - Extract snippets from ACTUAL file content (not assumptions)
   - Execute: python __ref/SOPs/agents-md-generator/executions/extract-context.py [TARGET_FOLDER_PATH] [TARGET_FOLDER]_analysis.json
   - Verify: [TARGET_FOLDER]_context.json created successfully

4. PHASE 3: Generate AGENTS.md Using Template
   - CRITICAL: Check for existing AGENTS.md first
     * Execute: python __ref/SOPs/agents-md-generator/executions/check-existing-agents-md.py [TARGET_FOLDER_PATH]
     * If exists and manually created: STOP - Report error, request user decision
     * If exists and tool-generated: Backup existing file, then proceed
     * If not exists: Proceed normally
   - CRITICAL: Load template file completely (don't rely on memory)
   - CRITICAL: Read actual source files (at least first 1000 words of each for Document Guide)
   - Systematically replace ALL placeholders line-by-line:
     * [FOLDER_TITLE] → From folder name or README (READ the README)
     * [FOLDER_DESCRIPTION] → From folder analysis AND actual README content
     * [FILE_PURPOSE] → From context JSON (verify matches actual file content)
     * [CONTAINS] → Extract from ACTUAL file content (read files, list sections)
     * [KEY_SECTIONS] → Extract from ACTUAL file headings (read files)
     * All other placeholders → Fill from JSON or actual files
   - ZERO assumptions: All content must come from JSON data or actual file content
   - If backup needed: Create backup (AGENTS.md.backup.[timestamp])
   - Write to: [TARGET_FOLDER]/AGENTS.md (only after confirmation if file exists)

5. PHASE 4: Validate Generated AGENTS.md
   - Execute: python __ref/SOPs/agents-md-generator/executions/validate-agents-md.py [TARGET_FOLDER]/AGENTS.md [TARGET_FOLDER_PATH]
   - Verify: All validation checks pass (exit code 0)

6. PHASE 5: Refine if Needed
   - If validation fails: Fix issues, re-validate (max 3 iterations)
   - If validation passes: Verify content quality manually:
     * Snippets match actual file content (read files to verify)
     * File purposes are specific (not "Documentation")
     * Document Guide sections match actual files (read files)
     * No assumptions in content

SUCCESS CRITERIA:
- AGENTS.md generated in target folder
- All validation checks pass (13/13)
- All placeholders replaced
- Content derived from actual files (0% assumptions)
- File inventory matches actual files
- CONTEXT section includes all 4 levels

Report completion status and any issues encountered.
```

---

## Example Usage

### Example 1: Generate for interview-framework folder

```
Generate AGENTS.md for folder=__ref/interview-framework using SOP at __ref/SOPs/agents-md-generator

CRITICAL: Follow the SOP workflow exactly:

1. PRE-FLIGHT (MANDATORY):
   - Read __ref/SOPs/agents-md-generator/directives/MISSION-OBJECTIVES.md
   - Read __ref/SOPs/agents-md-generator/directives/TASKER-ORDERS.md
   - Read __ref/SOPs/agents-md-generator/directives/AGENTS-MD-TEMPLATE.md
   - Read __ref/SOPs/agents-md-generator/directives/VALIDATION-CHECKLIST.md
   - Verify you understand the 5-phase workflow before proceeding

2. PHASE 1: Analyze Target Folder
   - Execute: python __ref/SOPs/agents-md-generator/executions/analyze-folder.py __ref/interview-framework
   - Verify: interview-framework_analysis.json created successfully

3. PHASE 2: Extract Context from Files
   - CRITICAL: Read at least first 500 words of EACH markdown file in target folder
   - Extract snippets from ACTUAL file content (not assumptions)
   - Execute: python __ref/SOPs/agents-md-generator/executions/extract-context.py __ref/interview-framework interview-framework_analysis.json
   - Verify: interview-framework_context.json created successfully

4. PHASE 3: Generate AGENTS.md Using Template
   - CRITICAL: Load template file completely (don't rely on memory)
   - CRITICAL: Read actual source files (at least first 1000 words of each for Document Guide)
   - Systematically replace ALL placeholders line-by-line
   - ZERO assumptions: All content must come from JSON data or actual file content
   - Write to: __ref/interview-framework/AGENTS.md

5. PHASE 4: Validate Generated AGENTS.md
   - Execute: python __ref/SOPs/agents-md-generator/executions/validate-agents-md.py __ref/interview-framework/AGENTS.md __ref/interview-framework
   - Verify: All validation checks pass (exit code 0)

6. PHASE 5: Refine if Needed
   - If validation fails: Fix issues, re-validate (max 3 iterations)
   - If validation passes: Verify content quality manually

SUCCESS CRITERIA:
- AGENTS.md generated in target folder
- All validation checks pass (13/13)
- All placeholders replaced
- Content derived from actual files (0% assumptions)

Report completion status and any issues encountered.
```

### Example 2: Generate for initial_scaffolding folder

```
Generate AGENTS.md for folder=__ref/initial_scaffolding using SOP at __ref/SOPs/agents-md-generator

[Use same structure as Example 1, replace folder path]
```

---

## One-Liner Version (Minimal)

For quick execution when you trust the agent knows the SOP:

```
Generate AGENTS.md for folder=[TARGET_FOLDER_PATH] following SOP at __ref/SOPs/agents-md-generator - MUST read all directives first, then execute 5 phases sequentially, validate, and ensure 0% assumptions in content.
```

---

## Terminal Command Version

If you prefer to run the scripts directly:

```bash
# Navigate to SOP directory
cd __ref/SOPs/agents-md-generator

# Phase 1: Analyze
python executions/analyze-folder.py [TARGET_FOLDER_PATH]

# Phase 2: Extract context
python executions/extract-context.py [TARGET_FOLDER_PATH] [TARGET_FOLDER]_analysis.json

# Phase 3: Generate (AI-assisted - use prompt above)
# [AI generates AGENTS.md using template]

# Phase 4: Validate
python executions/validate-agents-md.py [TARGET_FOLDER]/AGENTS.md [TARGET_FOLDER_PATH]
```

---

## Key Reminders

**CRITICAL REQUIREMENTS:**
- ✅ Read all directives BEFORE starting
- ✅ Read actual file contents (not just JSON)
- ✅ Use template systematically (line-by-line replacement)
- ✅ Zero assumptions (all content from JSON or files)
- ✅ Validate before delivery

**CONTENT QUALITY:**
- Snippets must match actual file content
- File purposes must be specific (not "Documentation")
- Document Guide must list actual sections from files
- Overview must come from actual README

---

**Version:** 1.1.0  
**Last Updated:** 2025-12-23  
**Status:** Production Ready

