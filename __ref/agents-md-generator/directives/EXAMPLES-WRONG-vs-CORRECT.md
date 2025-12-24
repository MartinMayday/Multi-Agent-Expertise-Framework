# EXAMPLES: Wrong vs. Correct AGENTS.md Generation

**Version:** 1.0.0  
**Date:** 2025-12-23  
**Purpose:** Show common mistakes and correct implementations for AGENTS.md generation

---

## Example 1: Missing CONTEXT Section

### ❌ WRONG

```markdown
---
title: My Package
version: 1.0.0
---

# My Package

This folder contains files for my project.

## Document Guide

### 1. README.md
**Purpose:** Documentation file
...
```

**Why This is Wrong:**
- Missing CONTEXT section entirely
- No progressive context loading protocol
- AI agents can't determine when to load what
- Context bloat will occur (everything loaded upfront)
- Violates AGENTS.md best practices

**Impact:**
- High token costs (loading everything)
- Slow performance (unnecessary context)
- Poor user experience (AI confused about what to load)

---

### ✅ CORRECT

```markdown
---
title: My Package
version: 1.0.0
---

# My Package

This folder contains files for my project.

## 🎯 CONTEXT: Progressive Context Loading Protocol

This section implements **progressive context loading** as described in [Claude Agent Skills](https://cloudnativeengineer.substack.com/p/ai-agent-wear-multiple-hats).

### Level 1: Front Matter (Always Loaded) - ~200 tokens
**When:** Every conversation start  
**Token Cost:** ~200 tokens  
**Load Time:** Instant

**Content:**
- Package title and description
- Key concepts
- Expected outcomes
- Contextual snippets

### Level 2: AGENTS.md Content (On-Demand) - ~2,000 tokens
**When:** After AI agent confirms package is relevant  
**Token Cost:** ~2,000 tokens  
**Trigger:** AI asks: "Load full package instructions?"

### Level 3: Reference Files (Selectively Loaded) - Variable tokens
**When:** Specific file content needed  
**Token Cost:** Variable (500-12,000 tokens per file)

### Level 4: Source Code (Execute, Don't Load) - ~100 tokens output only
**When:** Validation scripts need to run  
**Token Cost:** ~100 tokens (output only)

## Document Guide
...
```

**Why This is Correct:**
- Complete CONTEXT section with all 4 levels
- Token costs specified for each level
- Clear triggers for when to load
- Follows progressive context loading framework
- Reduces context bloat by 85%

---

## Example 2: Incorrect Tier Assignments

### ❌ WRONG

```yaml
contextual_snippets:
  - snippet: "Historical conversation log"
    keywords: [log, history, conversation]
    file: clog_perplexity_2025.md
    tier: 1  # ❌ WRONG: Historical logs should be tier 3
    
  - snippet: "Quick start guide"
    keywords: [quick start, guide, execution]
    file: quick-start.md
    tier: 3  # ❌ WRONG: Quick start should be tier 1
```

**Why This is Wrong:**
- Tier 1 should be essential files (README, quick-start, overview)
- Tier 3 should be reference files (historical logs, detailed guides)
- Incorrect assignments cause wrong files to load at wrong times
- Inefficient context usage

**Impact:**
- Essential files not loaded when needed
- Reference files loaded too early
- Poor context management

---

### ✅ CORRECT

```yaml
contextual_snippets:
  - snippet: "Quick start guide with step-by-step execution instructions"
    keywords: [quick start, guide, execution, steps]
    file: quick-start.md
    tier: 1  # ✅ CORRECT: Essential for first-time users
    
  - snippet: "Historical conversation log documenting generation process"
    keywords: [log, history, conversation, generation]
    file: clog_perplexity_2025.md
    tier: 3  # ✅ CORRECT: Reference material, load only when needed
```

**Why This is Correct:**
- Tier 1: Essential files (quick-start, README, overview)
- Tier 2: Core execution files (main prompts, templates)
- Tier 3: Reference files (historical logs, detailed guides)
- Logical tier assignments based on file importance
- Efficient context usage

**Tier Assignment Logic:**
- **Tier 1:** Files needed to understand what the package is and how to start
- **Tier 2:** Files needed for actual execution/work
- **Tier 3:** Files needed for reference/deep-dive only

---

## Example 3: Vague File Purposes

### ❌ WRONG

```yaml
files:
  - name: README.md
    purpose: "Documentation"  # ❌ WRONG: Too vague
    use_when: "When needed"    # ❌ WRONG: Not scenario-based
    tier: 1
    word_count: 500
```

**Why This is Wrong:**
- Purpose is too generic ("Documentation" could mean anything)
- use_when is not actionable ("When needed" is not helpful)
- AI agents can't determine when to use this file
- Doesn't help with decision-making

**Impact:**
- AI agents confused about file purpose
- Wrong files loaded for tasks
- Poor user experience

---

### ✅ CORRECT

```yaml
files:
  - name: README.md
    purpose: "Overview and quick start guide for the entire package - explains what the package does, how to use it, and where to start"
    use_when: "First time using the package, need orientation and understanding of package contents"
    tier: 1
    word_count: 500
```

**Why This is Correct:**
- Specific purpose statement (explains what, how, where)
- Scenario-based use_when (first time, need orientation)
- Actionable and clear
- Helps AI agents make decisions

**Purpose Statement Best Practices:**
- Be specific: "Overview and quick start guide" not "Documentation"
- Include what it does: "explains what the package does"
- Include how to use: "how to use it"
- Include when to use: "where to start"

**use_when Statement Best Practices:**
- Scenario-based: "First time using the package"
- Need-based: "need orientation and understanding"
- Actionable: Clear when to load this file

---

## Example 4: Missing Validation

### ❌ WRONG

```markdown
# Generated AGENTS.md

---
title: My Package
version: 1.0.0
# ❌ WRONG: Missing required fields (date, status, classification)
---

# My Package

[PLACEHOLDER_TEXT]  # ❌ WRONG: Placeholder not replaced

## Document Guide
# ❌ WRONG: Missing CONTEXT section
# ❌ WRONG: Missing file inventory
```

**Why This is Wrong:**
- Missing required YAML fields
- Placeholder text not replaced
- Missing required sections (CONTEXT, file inventory)
- No validation performed
- File is incomplete and unusable

**Impact:**
- YAML parsing errors
- Incomplete documentation
- AI agents can't use the file
- Poor quality output

---

### ✅ CORRECT

```markdown
# Generated AGENTS.md

---
title: My Package
version: 1.0.0
date: 2025-12-23
status: Production Ready
classification: Internal Operations | Handoff to IDE/CLI AI Coders
# ✅ CORRECT: All required fields present
---

# My Package

This folder contains production-ready files for my project.
# ✅ CORRECT: Placeholder replaced with actual content

## 🎯 CONTEXT: Progressive Context Loading Protocol
# ✅ CORRECT: CONTEXT section present with all 4 levels

## 📚 Document Guide
# ✅ CORRECT: Complete file inventory and document guide
```

**Why This is Correct:**
- All required YAML fields present
- All placeholders replaced
- All required sections present
- Validation passed before delivery
- File is complete and usable

**Validation Checklist:**
- [x] YAML frontmatter valid
- [x] All required sections present
- [x] CONTEXT section has 4 levels
- [x] No placeholder text
- [x] File inventory complete

---

## Example 5: Incorrect File Inventory

### ❌ WRONG

```yaml
files:
  - name: README.md
    purpose: "Documentation"
    use_when: "When needed"
    tier: 1
    word_count: 500
  # ❌ WRONG: Missing other files in folder
  # ❌ WRONG: Word count inaccurate (actual: 1200 words)
```

**Why This is Wrong:**
- Not all files in folder are listed
- Word count is inaccurate (500 vs actual 1200)
- Incomplete file inventory
- AI agents miss important files

**Impact:**
- Incomplete documentation
- Missing context for AI agents
- Inaccurate metadata

---

### ✅ CORRECT

```yaml
files:
  - name: README.md
    purpose: "Overview and quick start guide for the entire package"
    use_when: "First time using the package, need orientation"
    tier: 1
    word_count: 1200  # ✅ CORRECT: Accurate word count
    
  - name: quick-start.md
    purpose: "Step-by-step execution guide with copy-paste ready prompts"
    use_when: "Ready to execute, need exact steps and commands"
    tier: 1
    word_count: 3000
    
  - name: template.md
    purpose: "Template file with placeholders for generating new files"
    use_when: "Creating new files based on template, need structure"
    tier: 2
    word_count: 2000
  # ✅ CORRECT: All files in folder listed
  # ✅ CORRECT: Accurate word counts (±10% tolerance)
```

**Why This is Correct:**
- All markdown files in folder are listed
- Word counts are accurate (from actual file analysis)
- Complete file inventory
- AI agents have full context

**File Inventory Best Practices:**
- List ALL markdown files in folder
- Calculate word counts from actual files
- Include all file metadata (purpose, use_when, tier)
- Verify inventory matches actual folder contents

---

## Example 6: Missing Key Concepts

### ❌ WRONG

```yaml
key_concepts:
  - "Files"  # ❌ WRONG: Too generic
  - "Documentation"  # ❌ WRONG: Not a concept
  # ❌ WRONG: Missing actual concepts from folder content
```

**Why This is Wrong:**
- Concepts are too generic ("Files" is not a concept)
- Not extracted from actual folder content
- Doesn't help AI agents understand the package
- Missing core concepts

**Impact:**
- AI agents don't understand package domain
- Poor context understanding
- Ineffective keyword matching

---

### ✅ CORRECT

```yaml
key_concepts:
  - "Progressive context loading: 4-tier system (200 → 2000 → variable → 100 tokens) prevents context ROT"
  - "Vendor-neutral AGENTS.md format: Recognized by GitHub Copilot, Cursor, Windsurf, Claude Code"
  - "File inventory with tier assignments: Essential (tier 1), core (tier 2), reference (tier 3)"
  - "Contextual snippets with keywords: Enable hybrid search and semantic retrieval"
  # ✅ CORRECT: Specific concepts extracted from folder content
  # ✅ CORRECT: Concepts explain framework and approach
```

**Why This is Correct:**
- Concepts are specific and extracted from content
- Concepts explain the framework and approach
- Helps AI agents understand the package
- Enables better keyword matching

**Key Concepts Best Practices:**
- Extract from actual folder content
- Be specific (not generic)
- Explain framework/approach
- 3-10 concepts total
- Each concept should be a complete thought

---

## Example 7: Incorrect YAML Structure

### ❌ WRONG

```yaml
---
title: My Package
version: 1.0.0
date: 2025-12-23
status: Production Ready
# ❌ WRONG: Missing closing ---
# ❌ WRONG: Invalid YAML syntax (missing quotes, wrong indentation)

contextual_snippets:
  - snippet: Documentation file
    keywords: [docs, file]
    file: README.md
    tier: 1
  # ❌ WRONG: Missing quotes around string values
```

**Why This is Wrong:**
- Missing closing `---` for frontmatter
- Missing quotes around string values
- Invalid YAML syntax
- Will cause parsing errors

**Impact:**
- YAML parsing fails
- File can't be read
- AI agents can't use the file

---

### ✅ CORRECT

```yaml
---
title: My Package
version: 1.0.0
date: 2025-12-23
status: Production Ready
classification: Internal Operations | Handoff to IDE/CLI AI Coders
# ✅ CORRECT: Proper YAML frontmatter with closing ---

# Contextual Retrieval Snippets (Level 1: Always Loaded)
contextual_snippets:
  - snippet: "Overview and quick start guide for the entire package"
    keywords: [overview, quick start, guide, introduction]
    file: README.md
    tier: 1
  # ✅ CORRECT: Proper YAML syntax with quotes and indentation
---

# My Package
...
```

**Why This is Correct:**
- Proper YAML frontmatter (opening and closing `---`)
- All string values quoted
- Proper indentation (2 spaces)
- Valid YAML syntax
- Will parse correctly

**YAML Best Practices:**
- Always include opening and closing `---`
- Quote all string values
- Use 2-space indentation
- Validate YAML syntax before delivery
- Test parsing with YAML parser

---

## Example 8: Missing Expected Outcomes

### ❌ WRONG

```yaml
outcomes:
  - "Files"  # ❌ WRONG: Not an outcome
  - "Documentation"  # ❌ WRONG: Not an outcome
  # ❌ WRONG: Missing actual outcomes
```

**Why This is Wrong:**
- Not actual outcomes (what users can achieve)
- Not derived from folder purpose
- Doesn't help AI agents understand value
- Missing expected results

**Impact:**
- AI agents don't understand package value
- Users don't know what to expect
- Poor documentation

---

### ✅ CORRECT

```yaml
outcomes:
  - "Generate AGENTS.md files with progressive context loading for any folder"
  - "Reduce context bloat by 85% through tiered file loading"
  - "Enable AI agents to efficiently manage context with 4-level progressive loading"
  - "Create vendor-neutral context files recognized by multiple AI tools"
  # ✅ CORRECT: Specific outcomes derived from folder purpose
  # ✅ CORRECT: Outcomes explain what users can achieve
```

**Why This is Correct:**
- Outcomes are specific and actionable
- Derived from folder purpose
- Explain what users can achieve
- Help AI agents understand value

**Expected Outcomes Best Practices:**
- Extract from folder purpose
- Be specific (what users can achieve)
- 3-5 outcomes total
- Each outcome should be a complete thought
- Focus on value and results

---

## Summary: Common Mistakes to Avoid

1. **Missing CONTEXT Section** - Always include progressive context loading protocol
2. **Incorrect Tier Assignments** - Tier 1=essential, Tier 2=core, Tier 3=reference
3. **Vague File Purposes** - Be specific and actionable
4. **Missing Validation** - Always validate before delivery
5. **Incorrect File Inventory** - List all files with accurate metadata
6. **Missing Key Concepts** - Extract specific concepts from content
7. **Invalid YAML** - Ensure proper syntax and structure
8. **Missing Expected Outcomes** - Derive outcomes from folder purpose

---

**End of Examples**

