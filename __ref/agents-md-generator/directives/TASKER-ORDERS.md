# TASKER ORDERS: AGENTS.md Generation Execution Instructions

**Version:** 1.1.0  
**Date:** 2025-12-23  
**Classification:** Internal Operations | AI Agent Task Execution  
**Status:** Production Ready

**Changelog:**
- v1.1.0 (2025-12-23): Added mandatory directive reading, explicit file content requirements, content quality validation based on trial run findings
- v1.0.0 (2025-12-23): Initial release

---

## Executive Summary

This document provides step-by-step execution instructions for tasker-execution-agents to generate `AGENTS.md` files for any target folder. Follow these phases sequentially, validate at each step, and refine based on validation results.

**Expected Duration:** 5-15 minutes per folder (depending on file count)  
**Success Rate Target:** 95%+ first-pass generation with validation passing

---

## Pre-Flight Checklist

**CRITICAL: MANDATORY DIRECTIVE READING BEFORE STARTING**

Before starting execution, you MUST:

1. **Read MISSION-OBJECTIVES.md** (MANDATORY)
   - Understand mission statement
   - Review success criteria
   - Understand constraints
   - Know quality gates

2. **Read TASKER-ORDERS.md** (MANDATORY - this file)
   - Understand 5-phase workflow
   - Review each phase's requirements
   - Understand validation criteria

3. **Read AGENTS-MD-TEMPLATE.md** (MANDATORY)
   - Understand template structure
   - Review all placeholders
   - Understand replacement requirements

4. **Read EXAMPLES-WRONG-vs-CORRECT.md** (RECOMMENDED)
   - Learn from common mistakes
   - Understand correct implementations

5. **Read VALIDATION-CHECKLIST.md** (MANDATORY)
   - Understand all validation checks
   - Know what passes/fails

**VERIFICATION:** Before proceeding, confirm you have read all mandatory directives.

**Then verify:**
- [ ] Target folder path is valid and accessible
- [ ] Target folder contains at least one markdown file
- [ ] **Check for existing AGENTS.md** - Execute: `python executions/check-existing-agents-md.py [TARGET_FOLDER_PATH]`
  - If exists and manually created: **STOP** - Request user decision before proceeding
  - If exists and tool-generated: Plan to backup before overwrite
  - If not exists: Proceed normally
- [ ] Python 3.8+ is available
- [ ] All execution scripts are present in `executions/` folder
- [ ] Template file is present in `directives/AGENTS-MD-TEMPLATE.md`
- [ ] Validation script is present in `executions/validate-agents-md.py`

---

## Phase 1: Analyze Target Folder

**Objective:** Deep analysis of folder structure and files to extract metadata

**Execution:**
```bash
python executions/analyze-folder.py [TARGET_FOLDER_PATH]
```

**Expected Output:**
- JSON file: `[TARGET_FOLDER]_analysis.json`
- Contains: file metadata, structure, relationships, file types

**Validation:**
- [ ] JSON file created successfully
- [ ] All markdown files in folder are listed
- [ ] File metadata is accurate (size, word count, last modified)
- [ ] File types are identified correctly

**Error Handling:**
- **If folder not found:** Report error, exit with code 1
- **If no markdown files:** Report warning, ask user to confirm
- **If analysis fails:** Report error details, exit with code 1

**Decision Point:**
- If analysis succeeds → Proceed to Phase 2
- If analysis fails → Report error, stop execution

---

## Phase 2: Extract Context from Files

**Objective:** Extract contextual snippets, keywords, and determine tier assignments

**CRITICAL: MUST READ ACTUAL FILE CONTENTS**

Before running extraction script, you MUST:
1. Read at least the first 500 words of EACH markdown file in target folder
2. Extract actual snippets from file content (not from assumptions)
3. Verify snippets match actual file content

**Execution:**
```bash
python executions/extract-context.py [TARGET_FOLDER_PATH] [TARGET_FOLDER]_analysis.json
```

**Expected Output:**
- JSON file: `[TARGET_FOLDER]_context.json`
- Contains: contextual snippets, keywords, tier assignments, file purposes, use_when statements

**Content Source Verification:**
- [ ] Snippets extracted from actual file content (read files, not assumptions)
- [ ] Keywords extracted from file content (frontmatter, headings, text)
- [ ] File purposes derived from actual file content (not generic descriptions)
- [ ] use_when statements based on actual file content analysis

**Validation:**
- [ ] JSON file created successfully
- [ ] All files have contextual snippets (Level 1) - VERIFIED from actual content
- [ ] All files have keywords (minimum 3 per file) - EXTRACTED from content
- [ ] All files have tier assignments (1, 2, or 3)
- [ ] All files have specific purposes (not vague) - DERIVED from content
- [ ] All files have use_when statements (scenario-based) - BASED on content analysis

**Error Handling:**
- **If analysis file missing:** Report error, exit with code 1
- **If file read fails:** Report which file failed, continue with others
- **If extraction fails:** Report error details, exit with code 1

**Decision Point:**
- If extraction succeeds → Proceed to Phase 3
- If extraction fails → Report error, stop execution

---

## Phase 3: Generate AGENTS.md Using Template

**Objective:** Generate AGENTS.md file by filling template with extracted data

**CRITICAL: CHECK FOR EXISTING AGENTS.md BEFORE WRITING**

**Pre-Write Check:**
1. **Check if AGENTS.md already exists** in target folder
2. **If AGENTS.md exists:**
   - **Read existing file** to check if it was generated by this tool
   - **Check for tool signature** (look for "Generated by agents-md-generator" or similar in frontmatter)
   - **If generated by this tool:** Backup existing file (rename to `AGENTS.md.backup.[timestamp]`), then proceed
   - **If NOT generated by this tool:** **STOP and report error** - Do NOT overwrite manually created AGENTS.md files
   - **Report to user:** "AGENTS.md already exists. Options: (1) Backup and overwrite, (2) Abort, (3) Merge (not supported yet)"
   - **Wait for user confirmation** before proceeding

**CRITICAL: SYSTEMATIC TEMPLATE REPLACEMENT**

You MUST:
1. **Load template file** - Read `directives/AGENTS-MD-TEMPLATE.md` completely
2. **Load analysis JSON** - Read `[TARGET_FOLDER]_analysis.json`
3. **Load context JSON** - Read `[TARGET_FOLDER]_context.json`
4. **Read actual source files** - For Document Guide sections, read actual file content (at least first 1000 words of each file)
5. **Systematically replace placeholders** - Go through template line by line:
   - `[FOLDER_TITLE]` → Extract from folder name or first README (READ the README)
   - `[FOLDER_DESCRIPTION]` → Extract from folder analysis AND actual README content
   - `[KEY_CONCEPTS]` → Extract from context JSON AND verify against actual file content
   - `[FILE_NAME]` → From analysis JSON
   - `[FILE_PURPOSE]` → From context JSON (verify it matches actual file content)
   - `[TIER_ASSIGNMENT]` → From context JSON
   - `[FILE_METADATA]` → From analysis JSON
   - `[CONTAINS]` → Extract from ACTUAL file content (read files, list sections)
   - `[USE_WHEN_SCENARIO]` → Based on ACTUAL file content analysis
   - `[KEY_SECTIONS]` → Extract from ACTUAL file headings (read files)
   - All other placeholders → Fill from appropriate source (JSON or actual files)

**Content Source Requirements:**
- **0% assumptions** - All content must come from:
  - Analysis JSON (file metadata)
  - Context JSON (extracted snippets)
  - Actual file content (read files directly)
- **Document Guide sections** - MUST read actual file content to write "Contains" and "Key Sections"
- **Overview text** - MUST read README or main files to extract actual description

**Process:**
1. **Check for existing AGENTS.md** - Execute: `python executions/check-existing-agents-md.py [TARGET_FOLDER_PATH]`
2. **If AGENTS.md exists:**
   - Exit code 1 (tool-generated): Backup existing file, proceed with overwrite
   - Exit code 2 (manually created): **STOP** - Report error, request user decision
   - Exit code 0 (not exists): Proceed normally
3. Load template file (read completely, don't rely on memory)
4. Load analysis JSON
5. Load context JSON
6. **Read actual source files** (at least first 1000 words of each for Document Guide)
7. **Systematically replace placeholders** (one by one, verify each replacement)
8. Generate complete AGENTS.md content
9. **If backup needed:** Create backup of existing AGENTS.md (rename to `AGENTS.md.backup.[timestamp]`)
10. Write to `[TARGET_FOLDER]/AGENTS.md` (only after confirmation if file exists)

**Verification Before Writing:**
- [ ] Existing AGENTS.md checked and handled appropriately
- [ ] All placeholders replaced (search for `[` in output)
- [ ] Document Guide sections based on actual file content (not assumptions)
- [ ] Overview text extracted from actual README/content
- [ ] Key concepts verified against actual file content

**Validation:**
- [ ] AGENTS.md file created successfully
- [ ] All placeholders replaced (no `[PLACEHOLDER]` text remains)
- [ ] YAML frontmatter is valid
- [ ] All required sections present
- [ ] CONTEXT section includes all 4 levels

**Error Handling:**
- **If AGENTS.md exists and NOT generated by this tool:** Report error, stop execution, request user decision (backup/abort)
- **If AGENTS.md exists and generated by this tool:** Backup existing file, proceed with overwrite
- **If backup fails:** Report error, stop execution
- **If template missing:** Report error, exit with code 1
- **If JSON files missing:** Report error, exit with code 1
- **If placeholder replacement fails:** Report which placeholder, continue with others
- **If file write fails:** Report error, exit with code 1

**Decision Point:**
- If generation succeeds → Proceed to Phase 4
- If generation fails → Report error, stop execution

---

## Phase 4: Validate Generated AGENTS.md

**Objective:** Validate generated AGENTS.md against all requirements

**Execution:**
```bash
python executions/validate-agents-md.py [TARGET_FOLDER]/AGENTS.md [TARGET_FOLDER_PATH]
```

**Expected Output:**
- Validation report (stdout)
- Exit code: 0 = pass, 1 = fail

**Validation Checks:**
1. YAML frontmatter validity
2. All required sections present
3. CONTEXT section has 4 levels
4. Tier assignments are valid (1, 2, or 3)
5. No placeholder text remains
6. File inventory matches actual files
7. Word counts are reasonable
8. Keywords are relevant
9. **Content quality** - Snippets match actual file content (not generic)
10. **Content quality** - File purposes are specific (not vague like "Documentation")
11. **Content quality** - Document Guide sections reference actual file content

**Validation Report Format:**
```
✅ YAML frontmatter: PASS
✅ Required sections: PASS
✅ CONTEXT section: PASS
✅ Tier assignments: PASS
✅ No placeholders: PASS
✅ File inventory: PASS
✅ Word counts: PASS
✅ Keywords: PASS

Overall: PASS (8/8 checks)
```

**Error Handling:**
- **If validation fails:** Report which checks failed, provide details
- **If file not found:** Report error, exit with code 1
- **If validation script error:** Report error details, exit with code 1

**Decision Point:**
- If validation passes (exit code 0) → Proceed to Phase 5
- If validation fails (exit code 1) → Proceed to Phase 5 (refinement)

---

## Phase 5: Refine Based on Validation Results

**Objective:** Fix any issues identified during validation

**Process:**

**If Validation Passed:**
- [ ] Review generated AGENTS.md manually
- [ ] **Verify content is from files** - Check snippets match actual file content
- [ ] **Verify file purposes are specific** - Not vague like "Documentation", must be actionable
- [ ] **Verify use_when statements are actionable** - Scenario-based, not "When needed"
- [ ] **Verify tier assignments are logical** - Tier 1=essential, Tier 2=core, Tier 3=reference
- [ ] **Verify Document Guide sections** - "Contains" and "Key Sections" match actual files
- [ ] **Verify no assumptions** - All content traceable to JSON or actual files
- [ ] If all checks pass → **MISSION COMPLETE**

**If Validation Failed:**
1. Review validation report
2. Identify failed checks
3. For each failed check:
   - **YAML errors:** Fix syntax, re-validate
   - **Missing sections:** Add missing sections from template
   - **CONTEXT section issues:** Ensure all 4 levels are present
   - **Tier assignment issues:** Review tier logic, adjust assignments
   - **Placeholder text:** Replace remaining placeholders
   - **File inventory mismatches:** Update inventory to match actual files
   - **Word count issues:** Recalculate word counts
   - **Keyword issues:** Re-extract keywords from content
4. Re-run Phase 4 (validation)
5. Repeat until validation passes

**Refinement Limits:**
- Maximum 3 refinement iterations
- If validation still fails after 3 iterations → Report error, request human intervention

**Decision Point:**
- If refinement succeeds → **MISSION COMPLETE**
- If refinement fails after 3 iterations → Report error, stop execution

---

## Post-Execution Checklist

After successful generation:

- [ ] AGENTS.md file exists in target folder
- [ ] Validation passes (exit code 0)
- [ ] All placeholders replaced
- [ ] File inventory is accurate
- [ ] CONTEXT section is complete
- [ ] Clean up temporary files (analysis.json, context.json)

**Cleanup:**
```bash
# Optional: Remove temporary analysis files
rm [TARGET_FOLDER]_analysis.json
rm [TARGET_FOLDER]_context.json
```

---

## Error Recovery Procedures

### Error Type 1: Folder Not Found
**Action:** Verify folder path, check permissions, retry

### Error Type 2: No Markdown Files
**Action:** Report warning, ask user to confirm, proceed with empty inventory

### Error Type 3: Analysis Failure
**Action:** Check file permissions, verify Python version, review error logs

### Error Type 4: Context Extraction Failure
**Action:** Check file encoding, verify file readability, review error logs

### Error Type 5: Template Replacement Failure
**Action:** Verify template format, check JSON structure, review error logs

### Error Type 6: Existing AGENTS.md File
**Action:** 
- If generated by this tool: Backup existing file, proceed with overwrite
- If manually created: Report error, request user decision (backup/abort/merge)
- If user chooses abort: Stop execution
- If user chooses backup: Create backup, proceed with overwrite
- If user chooses merge: Report "Merge not supported yet", request backup/abort

### Error Type 7: Validation Failure
**Action:** Review validation report, fix issues, re-validate (max 3 iterations)

---

## Success Criteria

**Mission is successful when:**

1. ✅ AGENTS.md file generated in target folder
2. ✅ All validation checks pass (exit code 0)
3. ✅ All placeholders replaced
4. ✅ File inventory matches actual files
5. ✅ CONTEXT section includes all 4 levels
6. ✅ Tier assignments are logical
7. ✅ Documentation quality meets standards

**Status:** Ready for use by AI/LLM agents

---

## Execution Timeline

**Typical Execution Time:**
- Phase 1 (Analysis): 5-10 seconds
- Phase 2 (Extraction): 10-30 seconds
- Phase 3 (Generation): 2-5 seconds
- Phase 4 (Validation): 2-5 seconds
- Phase 5 (Refinement): 0-60 seconds (if needed)

**Total:** 5-15 minutes per folder (depending on file count and refinement needs)

---

## Notes for Tasker-Agents

**CRITICAL WORKFLOW REQUIREMENTS:**

1. **MUST read directives first** - Read MISSION-OBJECTIVES.md, TASKER-ORDERS.md, AGENTS-MD-TEMPLATE.md, VALIDATION-CHECKLIST.md before starting
2. **MUST read actual file contents** - Don't rely on JSON alone, read actual files for Document Guide sections
3. **MUST use template systematically** - Load template, replace placeholders one by one, don't generate from memory
4. **ZERO assumptions** - All content must come from JSON data or actual file content, not training data
5. **Always validate before delivery** - Never skip Phase 4
6. **Follow phases sequentially** - Don't skip phases
7. **Report errors clearly** - Include file paths, line numbers, error messages
8. **Clean up temporary files** - Remove analysis and context JSON files after completion
9. **Verify output location** - Ensure AGENTS.md is in the correct folder
10. **Check file permissions** - Ensure write permissions for target folder

**Content Quality Requirements:**
- Snippets must match actual file content (read files to verify)
- File purposes must be specific and actionable (not "Documentation")
- Document Guide "Contains" must list actual sections from files (read files)
- Document Guide "Key Sections" must list actual headings from files (read files)
- Overview text must come from actual README or main files (read files)

---

**End of Tasker Orders**

