# MISSION OBJECTIVES: AGENTS.md Generator SOP

**Version:** 1.0.0  
**Date:** 2025-12-23  
**Classification:** Internal Operations | AI Agent Task Execution  
**Status:** Production Ready

---

## Mission Statement

**Primary Mission:** Enable tasker-execution-agents to automatically generate production-ready `AGENTS.md` files for any folder, following progressive context loading principles and AGENTS.md best practices.

**Core Purpose:** Transform folder contents into structured, vendor-neutral context files that AI/LLM agents can use for efficient progressive context loading, reducing context bloat by 85% while maintaining complete traceability.

---

## Success Criteria

### Must-Have Requirements (Hard Constraints)

1. **Valid YAML Frontmatter**
   - All required fields present (title, version, date, status, classification)
   - Valid YAML syntax (no parsing errors)
   - Proper indentation and structure

2. **Complete Required Sections**
   - Contextual Retrieval Snippets (with tier assignments)
   - File Inventory (with purpose, use_when, tier, word_count)
   - Key Concepts (extracted from folder content)
   - Expected Outcomes (derived from folder purpose)
   - CONTEXT section (progressive loading protocol with 4 levels)
   - Document Guide (detailed breakdown of each file)
   - Quick Start workflow
   - Quality guarantees

3. **Progressive Context Loading Protocol**
   - Level 1: Front Matter (Always Loaded) - ~200 tokens
   - Level 2: AGENTS.md Content (On-Demand) - ~2,000 tokens
   - Level 3: Reference Files (Selectively Loaded) - Variable tokens
   - Level 4: Source Code (Execute, Don't Load) - ~100 tokens output only
   - All 4 levels must be documented with token costs, triggers, and content

4. **Proper Tier Assignments**
   - Tier 1: Essential files (README, quick-start, overview)
   - Tier 2: Core execution files (main prompts, templates)
   - Tier 3: Reference files (historical logs, detailed guides)
   - All tier assignments must be logical and consistent

5. **Accurate File Inventory**
   - All markdown files in folder must be listed
   - File purposes must be specific and actionable
   - use_when statements must be clear and scenario-based
   - Word counts must be accurate (±10% tolerance)

6. **No Placeholder Text**
   - All `[PLACEHOLDER]` text must be replaced
   - All `[FILL_ME]` sections must be completed
   - All template comments must be removed or converted to actual content

### Quality Standards (Soft Constraints)

1. **Keyword Relevance**
   - Keywords extracted from actual file content
   - Keywords match file purpose and domain
   - Minimum 3 keywords per file, maximum 10

2. **Concept Extraction**
   - Key concepts derived from folder content analysis
   - Concepts are specific, not generic
   - Minimum 3 concepts, maximum 10

3. **Documentation Quality**
   - Document Guide sections are comprehensive
   - Use When statements are specific and actionable
   - File purposes are clear and unambiguous

4. **Consistency**
   - Tier assignments follow consistent logic
   - File naming conventions are consistent
   - Formatting matches AGENTS.md best practices

---

## Constraints

### Format Constraints

1. **Must Follow AGENTS.md Format**
   - Vendor-neutral (not CLAUDE.md specific)
   - Recognized by GitHub Copilot, Cursor, Windsurf, Claude Code
   - Follows structured YAML frontmatter pattern

2. **Must Include CONTEXT Section**
   - Progressive context loading protocol is mandatory
   - All 4 levels must be documented
   - Token costs and triggers must be specified

3. **Must Be Markdown**
   - Valid Markdown syntax
   - Proper heading hierarchy (H1 → H2 → H3)
   - Code blocks properly formatted

### Content Constraints

1. **No Assumptions**
   - All content derived from actual folder files
   - No invented file purposes or descriptions
   - All metadata extracted from file analysis

2. **No Hardcoded Values**
   - Folder names, file names, paths must be dynamic
   - Word counts calculated from actual files
   - Tier assignments based on file analysis, not assumptions

3. **Vendor-Neutral Language**
   - Avoid tool-specific terminology
   - Use generic AI/LLM agent language
   - Follow AGENTS.md best practices

### Technical Constraints

1. **Python Scripts**
   - Standard library only (no external dependencies)
   - Python 3.8+ compatibility
   - Clear error messages and exit codes

2. **Validation**
   - All validation checks must pass before delivery
   - Exit code 0 = pass, 1 = fail
   - Validation report must be human-readable

3. **Performance**
   - Folder analysis completes in < 30 seconds for folders with < 50 files
   - Context extraction completes in < 60 seconds
   - Validation completes in < 10 seconds

---

## Quality Gates

### Pre-Delivery Validation

Before delivering a generated AGENTS.md file, the following must pass:

1. **YAML Validation**
   - [ ] Frontmatter parses without errors
   - [ ] All required fields present
   - [ ] No syntax errors

2. **Content Validation**
   - [ ] All required sections present
   - [ ] CONTEXT section has all 4 levels
   - [ ] No placeholder text remains
   - [ ] File inventory matches actual files

3. **Tier Assignment Validation**
   - [ ] All tiers are 1, 2, or 3
   - [ ] Tier assignments are logical
   - [ ] Tier 1 files are truly essential

4. **Metadata Validation**
   - [ ] Word counts are accurate (±10%)
   - [ ] File purposes are specific
   - [ ] use_when statements are actionable

5. **Format Validation**
   - [ ] Markdown syntax is valid
   - [ ] Code blocks are properly formatted
   - [ ] Links are valid (if present)

### Post-Delivery Verification

After delivery, verify:

1. **Usability**
   - [ ] AI agent can load Level 1 context successfully
   - [ ] Progressive loading works as documented
   - [ ] File inventory is accurate

2. **Completeness**
   - [ ] All files in folder are documented
   - [ ] All key concepts are captured
   - [ ] All expected outcomes are defined

---

## Failure Modes to Avoid

1. **Missing CONTEXT Section**
   - **Impact:** No progressive loading, context bloat
   - **Prevention:** Template includes CONTEXT section, validation checks for it

2. **Incorrect Tier Assignments**
   - **Impact:** Wrong files loaded at wrong times, inefficient context usage
   - **Prevention:** Heuristic-based tier assignment with validation

3. **Vague File Purposes**
   - **Impact:** AI agents can't determine when to use files
   - **Prevention:** Content analysis extracts specific purposes

4. **Remaining Placeholders**
   - **Impact:** Incomplete AGENTS.md, unusable
   - **Prevention:** Validation checks for placeholder patterns

5. **Missing Files in Inventory**
   - **Impact:** Incomplete documentation, missing context
   - **Prevention:** File analysis scans all markdown files

6. **Invalid YAML**
   - **Impact:** File can't be parsed, unusable
   - **Prevention:** YAML validation before delivery

---

## Success Metrics

### Quantitative Metrics

- **Validation Pass Rate:** 100% (all checks must pass)
- **File Coverage:** 100% (all markdown files documented)
- **Placeholder Removal:** 100% (no placeholders remain)
- **Tier Assignment Accuracy:** > 90% (logical assignments)

### Qualitative Metrics

- **File Purpose Clarity:** Specific and actionable (not vague)
- **use_when Statements:** Scenario-based and clear
- **Key Concepts:** Relevant and extracted from content
- **Documentation Quality:** Comprehensive and useful

---

## Mission Completion Criteria

A generated AGENTS.md file is considered **mission complete** when:

1. ✅ All validation checks pass (exit code 0)
2. ✅ All required sections are present and complete
3. ✅ CONTEXT section includes all 4 progressive loading levels
4. ✅ File inventory accurately reflects folder contents
5. ✅ Tier assignments are logical and consistent
6. ✅ No placeholder text remains
7. ✅ YAML frontmatter is valid
8. ✅ Documentation quality meets standards

**Status:** Ready for use by AI/LLM agents

---

**End of Mission Objectives**

