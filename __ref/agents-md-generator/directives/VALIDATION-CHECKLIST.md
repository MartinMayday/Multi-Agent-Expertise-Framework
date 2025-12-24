# VALIDATION CHECKLIST: AGENTS.md Quality Gates

**Version:** 1.0.0  
**Date:** 2025-12-23  
**Purpose:** Quality gates and validation criteria for generated AGENTS.md files

---

## Pre-Delivery Validation

Before delivering a generated AGENTS.md file, all checks below must pass. Use `executions/validate-agents-md.py` to automate these checks.

---

## 1. YAML Frontmatter Validation

### Check 1.1: YAML Syntax Validity
- [ ] YAML frontmatter parses without errors
- [ ] Opening `---` present
- [ ] Closing `---` present
- [ ] Proper indentation (2 spaces)
- [ ] No syntax errors (colons, quotes, brackets)

**Validation Method:** Parse YAML, catch exceptions  
**Error Message:** "YAML frontmatter syntax error: [details]"

### Check 1.2: Required Fields Present
- [ ] `title` field present
- [ ] `version` field present
- [ ] `date` field present
- [ ] `status` field present
- [ ] `classification` field present

**Validation Method:** Check field existence in parsed YAML  
**Error Message:** "Missing required field: [field_name]"

### Check 1.3: Field Value Validation
- [ ] `title` is non-empty string
- [ ] `version` matches pattern (e.g., "1.0.0")
- [ ] `date` is valid date format (YYYY-MM-DD)
- [ ] `status` is valid (e.g., "Production Ready")
- [ ] `classification` contains expected text

**Validation Method:** Validate field values against patterns  
**Error Message:** "Invalid field value: [field_name] = [value]"

---

## 2. Required Sections Validation

### Check 2.1: CONTEXT Section Present
- [ ] CONTEXT section exists (heading: "## 🎯 CONTEXT" or "## CONTEXT")
- [ ] Section is not empty
- [ ] Section contains progressive loading protocol

**Validation Method:** Search for CONTEXT section heading  
**Error Message:** "Missing CONTEXT section"

### Check 2.2: CONTEXT Section Completeness
- [ ] Level 1 (Front Matter) documented
- [ ] Level 2 (AGENTS.md Content) documented
- [ ] Level 3 (Reference Files) documented
- [ ] Level 4 (Source Code) documented
- [ ] All 4 levels have token costs specified
- [ ] All 4 levels have triggers specified

**Validation Method:** Search for "Level 1", "Level 2", "Level 3", "Level 4"  
**Error Message:** "CONTEXT section missing level [X]"

### Check 2.3: Document Guide Section Present
- [ ] Document Guide section exists
- [ ] Section contains file breakdowns
- [ ] At least one file documented

**Validation Method:** Search for "Document Guide" heading  
**Error Message:** "Missing Document Guide section"

### Check 2.4: File Inventory Section Present
- [ ] File inventory exists in YAML frontmatter
- [ ] `files:` array present
- [ ] At least one file listed

**Validation Method:** Check YAML for `files:` array  
**Error Message:** "Missing file inventory"

### Check 2.5: Contextual Snippets Present
- [ ] `contextual_snippets:` array present in YAML
- [ ] At least one snippet listed
- [ ] Each snippet has required fields

**Validation Method:** Check YAML for `contextual_snippets:` array  
**Error Message:** "Missing contextual snippets"

---

## 3. Tier Assignment Validation

### Check 3.1: Tier Values Valid
- [ ] All tier assignments are 1, 2, or 3
- [ ] No tier values outside valid range
- [ ] No missing tier assignments

**Validation Method:** Validate tier values in contextual_snippets and files  
**Error Message:** "Invalid tier assignment: [tier_value] (must be 1, 2, or 3)"

### Check 3.2: Tier Assignment Logic
- [ ] Tier 1 files are essential (README, quick-start, overview)
- [ ] Tier 2 files are core execution files
- [ ] Tier 3 files are reference files
- [ ] Tier assignments are consistent across contextual_snippets and files

**Validation Method:** Heuristic check based on file names and purposes  
**Error Message:** "Tier assignment may be incorrect: [file_name] assigned tier [tier]"

**Note:** This is a warning, not an error (heuristic-based)

---

## 4. Placeholder Text Validation

### Check 4.1: No Placeholder Patterns
- [ ] No `[PLACEHOLDER]` text remains
- [ ] No `[FILL_ME]` text remains
- [ ] No `[REPLACE]` text remains
- [ ] No `[EXAMPLE]` text remains
- [ ] No `[CHANGE_ME]` text remains

**Validation Method:** Search for common placeholder patterns  
**Error Message:** "Placeholder text found: [placeholder_text] at line [line_number]"

### Check 4.2: No Template Comments
- [ ] No `# REPLACE:` comments
- [ ] No `# EXTRACT:` comments
- [ ] No `# ADD MORE:` comments
- [ ] No `# PLACEHOLDER REPLACEMENT GUIDE` section

**Validation Method:** Search for template comment patterns  
**Error Message:** "Template comment found: [comment] at line [line_number]"

**Note:** Some comments are acceptable (explanatory), but template-specific comments should be removed

---

## 5. File Inventory Validation

### Check 5.1: File Inventory Completeness
- [ ] All markdown files in folder are listed
- [ ] No extra files listed (not in folder)
- [ ] File names match actual files

**Validation Method:** Compare file inventory with actual folder contents  
**Error Message:** "File inventory mismatch: [file_name] [missing/extra]"

### Check 5.2: File Metadata Completeness
- [ ] Each file has `name` field
- [ ] Each file has `purpose` field
- [ ] Each file has `use_when` field
- [ ] Each file has `tier` field
- [ ] Each file has `word_count` field

**Validation Method:** Check each file entry for required fields  
**Error Message:** "File [file_name] missing field: [field_name]"

### Check 5.3: File Purpose Quality
- [ ] File purposes are specific (not vague like "Documentation")
- [ ] File purposes are actionable (explain what file does)
- [ ] File purposes are not empty

**Validation Method:** Heuristic check for vague purposes  
**Error Message:** "File purpose may be too vague: [file_name] = [purpose]"

**Note:** This is a warning, not an error (heuristic-based)

### Check 5.4: use_when Statement Quality
- [ ] use_when statements are scenario-based (not "When needed")
- [ ] use_when statements are specific
- [ ] use_when statements are not empty

**Validation Method:** Heuristic check for vague use_when  
**Error Message:** "use_when statement may be too vague: [file_name] = [use_when]"

**Note:** This is a warning, not an error (heuristic-based)

### Check 5.5: Word Count Accuracy
- [ ] Word counts are accurate (±10% tolerance)
- [ ] Word counts are positive integers
- [ ] Word counts match actual file sizes

**Validation Method:** Compare word counts with actual file analysis  
**Error Message:** "Word count inaccurate: [file_name] = [count] (expected: [expected] ±10%)"

---

## 6. Contextual Snippets Validation

### Check 6.1: Snippet Completeness
- [ ] Each snippet has `snippet` field
- [ ] Each snippet has `keywords` field
- [ ] Each snippet has `file` field
- [ ] Each snippet has `tier` field

**Validation Method:** Check each snippet entry for required fields  
**Error Message:** "Snippet for [file_name] missing field: [field_name]"

### Check 6.2: Keyword Quality
- [ ] Each snippet has 3-10 keywords
- [ ] Keywords are relevant to file content
- [ ] Keywords are not empty strings

**Validation Method:** Check keyword count and relevance  
**Error Message:** "Snippet for [file_name] has invalid keywords: [keywords]"

**Note:** Relevance check is heuristic-based (warning, not error)

### Check 6.3: Snippet Text Quality
- [ ] Snippet text is not empty
- [ ] Snippet text is specific (not generic)
- [ ] Snippet text matches file purpose

**Validation Method:** Check snippet text length and content  
**Error Message:** "Snippet for [file_name] may be too generic: [snippet]"

**Note:** This is a warning, not an error (heuristic-based)

---

## 7. Key Concepts Validation

### Check 7.1: Key Concepts Present
- [ ] `key_concepts:` array present in YAML
- [ ] At least 3 concepts listed
- [ ] Maximum 10 concepts listed

**Validation Method:** Check YAML for `key_concepts:` array  
**Error Message:** "Key concepts missing or invalid count: [count] (expected: 3-10)"

### Check 7.2: Concept Quality
- [ ] Concepts are specific (not generic like "Files")
- [ ] Concepts are extracted from folder content
- [ ] Concepts are not empty strings

**Validation Method:** Heuristic check for generic concepts  
**Error Message:** "Key concept may be too generic: [concept]"

**Note:** This is a warning, not an error (heuristic-based)

---

## 8. Expected Outcomes Validation

### Check 8.1: Expected Outcomes Present
- [ ] `outcomes:` array present in YAML
- [ ] At least 3 outcomes listed
- [ ] Maximum 5 outcomes listed

**Validation Method:** Check YAML for `outcomes:` array  
**Error Message:** "Expected outcomes missing or invalid count: [count] (expected: 3-5)"

### Check 8.2: Outcome Quality
- [ ] Outcomes are specific (what users can achieve)
- [ ] Outcomes are derived from folder purpose
- [ ] Outcomes are not empty strings

**Validation Method:** Heuristic check for generic outcomes  
**Error Message:** "Expected outcome may be too generic: [outcome]"

**Note:** This is a warning, not an error (heuristic-based)

---

## 9. Markdown Format Validation

### Check 9.1: Markdown Syntax
- [ ] Valid Markdown syntax
- [ ] Proper heading hierarchy (H1 → H2 → H3)
- [ ] Code blocks properly formatted (triple backticks)
- [ ] Links are valid (if present)

**Validation Method:** Basic Markdown syntax check  
**Error Message:** "Markdown syntax error: [details]"

### Check 9.2: Section Structure
- [ ] Headings are properly formatted
- [ ] Sections are not empty
- [ ] Content flows logically

**Validation Method:** Check heading structure and content  
**Error Message:** "Section structure issue: [details]"

---

## 10. Consistency Validation

### Check 10.1: Tier Consistency
- [ ] Tier assignments match between contextual_snippets and files
- [ ] Same file has same tier in both places

**Validation Method:** Compare tier assignments  
**Error Message:** "Tier inconsistency: [file_name] has tier [tier1] in snippets, [tier2] in files"

### Check 10.2: File Name Consistency
- [ ] File names match between contextual_snippets and files
- [ ] File names match actual files in folder

**Validation Method:** Compare file names across sections  
**Error Message:** "File name inconsistency: [file_name] [details]"

---

## 11. Content Quality Validation (CRITICAL)

**Purpose:** Ensure content is derived from actual files, not assumptions or training data.

### Check 11.1: Snippet Content Verification
- [ ] Snippets match actual file content (not generic descriptions)
- [ ] Snippets are extracted from file content (read files to verify)
- [ ] Snippets are not assumptions (e.g., "Documentation file" is too generic)

**Validation Method:** 
1. Read actual file content (first 500 words)
2. Compare snippet text with file content
3. Check if snippet appears in file or is clearly derived from it

**Error Message:** "Snippet for [file_name] may not match actual file content: [snippet]"

**Note:** This is a warning, not an error (requires manual verification)

### Check 11.2: File Purpose Specificity
- [ ] File purposes are specific (not vague like "Documentation", "Guide", "File")
- [ ] File purposes are actionable (explain what file does, not just what it is)
- [ ] File purposes are derived from actual file content

**Validation Method:** Heuristic check for vague purposes:
- Vague: "Documentation", "Guide", "File", "Content", "Information"
- Specific: "Complete 5-phase interview methodology for extracting context", "Quick reference card with five questions"

**Error Message:** "File purpose too vague: [file_name] = '[purpose]' (should be specific and actionable)"

**Note:** This is a warning, not an error (heuristic-based)

### Check 11.3: Document Guide Content Verification
- [ ] Document Guide "Contains" sections list actual file sections (read files to verify)
- [ ] Document Guide "Key Sections" list actual headings from files (read files to verify)
- [ ] Document Guide content is not generic (not "Various sections", "Multiple topics")

**Validation Method:**
1. Read actual file content (first 1000 words)
2. Extract actual headings/sections
3. Compare with Document Guide content

**Error Message:** "Document Guide for [file_name] may not match actual file content (verify by reading file)"

**Note:** This is a warning, not an error (requires manual verification)

### Check 11.4: Overview Text Source Verification
- [ ] Overview text is extracted from actual README or main files (not assumptions)
- [ ] Overview text matches actual folder purpose (read README to verify)
- [ ] Overview text is not generic (not "Collection of files", "Documentation folder")

**Validation Method:**
1. Read README.md or main file in folder
2. Compare overview text with actual file content
3. Check if overview is clearly derived from files

**Error Message:** "Overview text may not match actual folder content (verify by reading README)"

**Note:** This is a warning, not an error (requires manual verification)

### Check 11.5: Key Concepts Source Verification
- [ ] Key concepts are extracted from actual file content (not generic concepts)
- [ ] Key concepts are specific to folder content (not "files", "documentation", "markdown")
- [ ] Key concepts match actual folder purpose (read files to verify)

**Validation Method:** Heuristic check for generic concepts:
- Generic: "files", "documentation", "markdown", "content", "information"
- Specific: "Five-phase interview methodology", "Progressive context loading", "Context extraction"

**Error Message:** "Key concept may be too generic: '[concept]' (should be specific to folder content)"

**Note:** This is a warning, not an error (heuristic-based)

---

## Validation Report Format

### Pass Report
```
✅ YAML frontmatter: PASS
✅ Required sections: PASS
✅ CONTEXT section: PASS (4 levels)
✅ Tier assignments: PASS
✅ No placeholders: PASS
✅ File inventory: PASS ([X] files)
✅ Word counts: PASS
✅ Keywords: PASS
✅ Key concepts: PASS ([X] concepts)
✅ Expected outcomes: PASS ([X] outcomes)
✅ Markdown format: PASS
✅ Consistency: PASS
✅ Content quality: PASS (snippets verified, purposes specific, Document Guide verified)

Overall: PASS (13/13 checks)
```

### Fail Report
```
❌ YAML frontmatter: FAIL
  - Missing required field: date
  - Invalid field value: version = "1.0" (expected pattern: "X.Y.Z")

✅ Required sections: PASS
❌ CONTEXT section: FAIL
  - Missing level 4 (Source Code)

⚠️  Tier assignments: WARNING
  - Tier assignment may be incorrect: README.md assigned tier 3 (expected: tier 1)

❌ No placeholders: FAIL
  - Placeholder text found: [FILL_ME] at line 45

Overall: FAIL (3/12 checks passed, 1 warning)
```

---

## Exit Codes

- **0:** All checks passed (ready for delivery)
- **1:** One or more checks failed (needs refinement)

---

## Validation Execution

Run validation:
```bash
python executions/validate-agents-md.py [TARGET_FOLDER]/AGENTS.md [TARGET_FOLDER_PATH]
```

**Expected Output:**
- Validation report (stdout)
- Exit code (0 = pass, 1 = fail)

---

## Post-Validation Actions

### If Validation Passes
- [ ] Review generated AGENTS.md manually
- [ ] **Verify content is from files** - Check snippets match actual file content (read files)
- [ ] **Verify file purposes are specific** - Not vague like "Documentation", must be actionable
- [ ] **Verify use_when statements are actionable** - Scenario-based, not "When needed"
- [ ] **Verify tier assignments are logical** - Tier 1=essential, Tier 2=core, Tier 3=reference
- [ ] **Verify Document Guide sections** - "Contains" and "Key Sections" match actual files (read files)
- [ ] **Verify no assumptions** - All content traceable to JSON or actual files
- [ ] **Ready for delivery**

### If Validation Fails
1. Review validation report
2. Fix failed checks
3. Re-run validation
4. Repeat until all checks pass (max 3 iterations)

---

**End of Validation Checklist**

