---
title: [FOLDER_TITLE]
version: [VERSION]
author: [AUTHOR]
date: [DATE]
status: [STATUS]
classification: Internal Operations | Handoff to IDE/CLI AI Coders
framework: [FRAMEWORK]
project: [PROJECT_NAME]
output_expected: [OUTPUT_EXPECTED]
execution_time: [EXECUTION_TIME]

# Contextual Retrieval Snippets (Level 1: Always Loaded)
# REPLACE: [FILE_NAME], [FILE_PURPOSE], [KEYWORDS], [TIER_ASSIGNMENT]
# EXTRACT: From context extraction JSON, one snippet per file
contextual_snippets:
  - snippet: "[FILE_PURPOSE - first sentence or summary]"
    keywords: [KEYWORDS - array of 3-10 relevant keywords]
    file: [FILE_NAME]
    tier: [TIER_ASSIGNMENT - 1, 2, or 3]
  # ADD MORE: One entry per markdown file in folder

# File Inventory
# REPLACE: [FILE_NAME], [FILE_PURPOSE], [USE_WHEN], [TIER_ASSIGNMENT], [WORD_COUNT]
# EXTRACT: From analysis and context JSON files
files:
  - name: [FILE_NAME]
    purpose: "[FILE_PURPOSE - specific and actionable, not vague]"
    use_when: "[USE_WHEN - scenario-based, clear when to use this file]"
    tier: [TIER_ASSIGNMENT - 1=essential, 2=core, 3=reference]
    word_count: [WORD_COUNT - actual word count from file analysis]
  # ADD MORE: One entry per markdown file in folder

# Key Concepts
# REPLACE: [KEY_CONCEPTS]
# EXTRACT: From folder content analysis, identify 3-10 core concepts
# FORMAT: Each concept as a quoted string, one per line
key_concepts:
  - "[KEY_CONCEPT_1 - specific concept extracted from folder content]"
  - "[KEY_CONCEPT_2 - another core concept]"
  - "[KEY_CONCEPT_3 - continue as needed]"
  # ADD MORE: 3-10 concepts total, extracted from actual content

# Expected Outcomes
# REPLACE: [OUTCOMES]
# EXTRACT: From folder purpose and content analysis
# FORMAT: Each outcome as a quoted string, one per line
outcomes:
  - "[OUTCOME_1 - what users can achieve with this package]"
  - "[OUTCOME_2 - another expected result]"
  - "[OUTCOME_3 - continue as needed]"
  # ADD MORE: 3-5 outcomes total, derived from folder purpose
---

# [FOLDER_TITLE]

**[FOLDER_DESCRIPTION - one sentence summary of what this folder contains]**

**Version:** [VERSION]  
**Status:** [STATUS]  
**Framework:** [FRAMEWORK - if applicable]  
**Target:** [TARGET - what this package is for]

---

## 📋 Overview

[OVERVIEW_TEXT - 2-3 paragraphs explaining what this folder contains, its purpose, and key features. Extract from folder analysis and README files if present.]

**Core Purpose:** [CORE_PURPOSE - one sentence describing the primary purpose]

**Key Outcome:** [KEY_OUTCOME - one sentence describing the expected result]

---

## 🎯 CONTEXT: Progressive Context Loading Protocol

This section implements **progressive context loading** as described in [Claude Agent Skills: Teaching Your AI Agent to Wear Multiple Hats](https://cloudnativeengineer.substack.com/p/ai-agent-wear-multiple-hats?open=false#%C2%A7how-progressive-context-loading-works). Context loads in stages to prevent bloat and ensure only relevant information is loaded when needed.

### Level 1: Front Matter (Always Loaded) - ~200 tokens

**When:** Every conversation start  
**Token Cost:** ~200 tokens  
**Load Time:** Instant

**Content:**
- Package title and description (from YAML frontmatter)
- Key concepts (one-line summaries)
- Expected outcomes (bullet points)
- Contextual snippets (brief descriptions only)

**Purpose:** AI agent decides "Should I use this package?" without loading full content.

**Example:**
```yaml
contextual_snippets:
  - snippet: "[EXAMPLE_SNIPPET - brief description]"
    keywords: [EXAMPLE_KEYWORDS]
    file: [EXAMPLE_FILE]
    tier: 1
```

---

### Level 2: AGENTS.md Content (On-Demand) - ~2,000 tokens

**When:** After AI agent confirms package is relevant  
**Token Cost:** ~2,000 tokens  
**Load Time:** < 1 second  
**Trigger:** AI asks: "Load full package instructions? (Takes ~2000 tokens)"

**Content:**
- Complete file inventory with purpose and use_when
- Document Guide section (detailed breakdown of each file)
- Quick Start workflow
- Key principles and quality guarantees
- Execution checklist

**Purpose:** Full package instructions without loading individual file contents.

**What's Included:**
- File descriptions (purpose, use_when, tier, word_count)
- Document Guide for each file (Purpose, Contains, Use When, Key Sections)
- Execution workflow diagram
- Quality guarantees table
- Key principles

**What's NOT Included:**
- Full content of individual files
- Detailed code examples
- Complete templates

---

### Level 3: Reference Files (Selectively Loaded) - Variable tokens

**When:** Specific file content needed during execution  
**Token Cost:** Variable (500-12,000 tokens per file)  
**Load Time:** < 1 second per file  
**Trigger:** AI asks: "Load [filename] for [specific task]? (Takes ~X tokens)"

**Content:**
- Individual file contents loaded only when referenced
- Detailed guides, templates, examples
- Complete specifications and frameworks

**File Loading Tiers:**

**Tier 1 Files (Load First - Essential):**
[TIER_1_FILES - list files with tier 1, include word counts]
- `[FILE_NAME]` (~[WORD_COUNT] words) - [BRIEF_PURPOSE]

**Tier 2 Files (Load on Demand - Core Execution):**
[TIER_2_FILES - list files with tier 2, include word counts]
- `[FILE_NAME]` (~[WORD_COUNT] words) - [BRIEF_PURPOSE]

**Tier 3 Files (Load Only When Needed - Historical/Reference):**
[TIER_3_FILES - list files with tier 3, include word counts]
- `[FILE_NAME]` (~[WORD_COUNT] words) - [BRIEF_PURPOSE]

**Purpose:** Detailed content appears only when explicitly needed, keeping context clean.

**Example Loading Sequence:**
```
User: "I need to execute Phase 1"
↓
AI: "Load [TIER_1_FILE]? (Takes ~[WORD_COUNT] tokens)"
↓
User: "Yes"
↓
AI loads: [TIER_1_FILE] (Level 3)
↓
AI: "Load [TIER_2_FILE] Phase 1 section? (Takes ~[WORD_COUNT] tokens)"
↓
User: "Yes"
↓
AI loads: Phase 1 section only (Level 3, selective)
```

---

### Level 4: Source Code (Execute, Don't Load) - ~100 tokens output only

**When:** Validation scripts need to run  
**Token Cost:** ~100 tokens (output only, code not loaded)  
**Load Time:** Execution time (varies)  
**Trigger:** AI executes: `python validation/validate-story-file.py story.md`

**Content:**
- Python validation scripts (execute, don't load to context)
- Script output (success/failure messages)
- Metrics and reports (generated data)

**Purpose:** Complex logic stays external, keeping context window clean.

**What's Executed:**
[LIST_SCRIPTS - if folder contains Python scripts, list them here]
- `[SCRIPT_NAME].py` - [SCRIPT_PURPOSE]

**What's Loaded:**
- Only script output (✅/❌, error messages, metrics)
- Never the script source code itself

**Example:**
```bash
# AI executes (code not loaded to context):
python validation/validate-story-file.py stories/story_city001.md

# AI sees only output (~100 tokens):
✅ Valid - All 7 sections present, testable
Section 1: REQUIREMENTS ✅
Section 2: DESIGN DECISIONS ✅
...
```

---

### Progressive Loading Summary

| Level | Content | Token Cost | When | Trigger |
|-------|---------|------------|------|---------|
| **1. Front Matter** | Brief description, keywords | ~200 | Always | Automatic |
| **2. AGENTS.md** | Full package instructions | ~2,000 | On-demand | AI confirms relevance |
| **3. Reference Files** | Individual file contents | 500-12,000 | Selective | AI asks per file |
| **4. Source Code** | Script execution output | ~100 | As needed | AI executes scripts |

**Total Maximum Context:** ~[MAX_TOKENS] tokens (if all files loaded)  
**Typical Context:** ~2,200 tokens (Level 1 + Level 2 only)  
**Context Savings:** [SAVINGS_PERCENT]% reduction vs. loading everything upfront

---

## 📚 Document Guide

# REPLACE: [FILE_NAME], [FILE_PURPOSE], [CONTAINS], [USE_WHEN], [KEY_SECTIONS], [TIER], [WORD_COUNT]
# GENERATE: One Document Guide section per file in folder
# FORMAT: Follow the pattern below for each file

### 1. **[FILE_NAME]** — [FILE_PURPOSE_SHORT]

**Purpose:** [FILE_PURPOSE - full purpose statement]

**Contains:**
- [CONTAINS_ITEM_1 - main content element]
- [CONTAINS_ITEM_2 - another content element]
- [CONTAINS_ITEM_3 - continue as needed]
- [ADD_MORE - extract from actual file content]

**Use When:**
- [USE_WHEN_SCENARIO_1 - specific scenario]
- [USE_WHEN_SCENARIO_2 - another scenario]
- [USE_WHEN_SCENARIO_3 - continue as needed]

**Key Sections:**
- [KEY_SECTION_1 - main section name]
- [KEY_SECTION_2 - another section]
- [KEY_SECTION_3 - continue as needed]

**Context Loading Tier:** [TIER_ASSIGNMENT] ([TIER_DESCRIPTION])

**Word Count:** ~[WORD_COUNT] words

---

# REPEAT: Generate one Document Guide section for each file in folder
# Use the same format as above for each file

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Load Level 1 Context (Automatic)
AI agent automatically loads front matter:
- Package description
- Key concepts
- Expected outcomes
- Contextual snippets

**Token Cost:** ~200 tokens  
**Time:** Instant

### Step 2: Confirm Package Relevance
AI asks: "This package [BRIEF_DESCRIPTION]. Should I load full instructions? (~2000 tokens)"

**If Yes:** Proceed to Step 3  
**If No:** AI suggests alternative or asks for clarification

### Step 3: Load Level 2 Context (On-Demand)
AI loads full AGENTS.md content:
- Complete file inventory
- Document Guide
- Quick Start workflow
- Key principles

**Token Cost:** ~2,000 tokens  
**Time:** < 1 second

### Step 4: Execute Based on Need
**For Execution:**
1. AI loads [TIER_1_FILE] (Level 3, ~[WORD_COUNT] tokens)
2. AI loads [TIER_2_FILE] specific section (Level 3, ~[WORD_COUNT] tokens)
3. Execute task
4. Continue with additional files as needed

**For Reference:**
1. AI loads [TIER_3_FILE] specific section (Level 3, variable tokens)
2. AI loads [ANOTHER_FILE] if overview needed (Level 3, variable tokens)

**For Validation:**
1. AI executes validation scripts (Level 4, ~100 tokens output only)
2. AI sees results, code not loaded to context

---

## 📊 Expected Output Structure

[OUTPUT_STRUCTURE - if applicable, describe what this package generates or contains. Extract from folder analysis.]

**Total:** [FILE_COUNT] files, ~[TOTAL_WORDS] words, [QUALITY_STANDARD]

---

## ✅ Quality Guarantees

| Guarantee | Standard | Enforcement |
|-----------|----------|-------------|
| **No Context ROT** | 0% hallucinations | [VALIDATION_METHOD] |
| **Progressive Loading** | 4-level system | CONTEXT section |
| **Complete Documentation** | All files documented | File inventory |
| **Accurate Metadata** | ±10% word count tolerance | Validation scripts |

---

## 🚀 Key Principles

### 1. PROGRESSIVE CONTEXT LOADING
Context loads in stages (prevent ROT):
- **Level 1:** Front matter (200 tokens) - Always loaded
- **Level 2:** AGENTS.md content (2,000 tokens) - On-demand
- **Level 3:** Reference files (500-12,000 tokens) - Selective
- **Level 4:** Source code execution (~100 tokens output) - Execute, don't load

### 2. VENDOR-NEUTRAL
Follow AGENTS.md best practices:
- Recognized by GitHub Copilot, Cursor, Windsurf, Claude Code
- No tool-specific terminology
- Generic AI/LLM agent language

### 3. COMPLETE DOCUMENTATION
Every file documented:
- Specific purpose (not vague)
- Scenario-based use_when statements
- Accurate metadata (word counts, tiers)

---

## 📋 Execution Checklist

**Before starting:**
- [ ] All files downloaded/accessible
- [ ] Read overview (10 min)
- [ ] Understand progressive loading protocol
- [ ] Ready to execute

**After execution:**
- [ ] All files loaded as needed
- [ ] Progressive loading worked correctly
- [ ] Context savings achieved
- [ ] Mission complete

---

## 📞 Support

During execution, if you get stuck:

1. **Check Document Guide** - Detailed file breakdowns
2. **Review CONTEXT section** - Progressive loading protocol
3. **Reference file inventory** - Find right file for task
4. **Check tier assignments** - Load files in correct order

---

## 🎯 Success Signal

When AI agent successfully uses this package:

```
✅ Level 1 context loaded (200 tokens)
✅ Level 2 context loaded (2000 tokens)
✅ Level 3 files loaded selectively as needed
✅ Context savings: [PERCENT]% reduction
✅ Mission complete
```

**Status:** Ready for use by AI/LLM agents

---

## 📚 File Reference Quick Links

[QUICK_LINKS - generate links to all files in folder]
- **[Start Here]:** `[TIER_1_FILE]`
- **[Execute This]:** `[TIER_2_FILE]`
- **[Reference This]:** `[TIER_3_FILE]`
- **[Add More]:** `[OTHER_FILES]`

---

## 📖 References

- [Claude Agent Skills: Teaching Your AI Agent to Wear Multiple Hats](https://cloudnativeengineer.substack.com/p/ai-agent-wear-multiple-hats?open=false#%C2%A7how-progressive-context-loading-works) - Progressive context loading framework
- [Equipping Agents for the Real World with Agent Skills](https://www.anthropic.com/research/equipping-agents) - Anthropic's official skills architecture
- [Agent Skills Best Practices](https://docs.anthropic.com/claude/docs/agent-skills) - Official documentation

---

**Generated:** [DATE]  
**Status:** [STATUS]  
**Quality:** Progressive context loading, complete traceability  
**Next:** Use by AI/LLM agents for efficient context management

**Ready for use.** 🚀

---

# PLACEHOLDER REPLACEMENT GUIDE

## YAML Frontmatter Placeholders
- `[FOLDER_TITLE]` - Extract from folder name or first README title
- `[VERSION]` - Use "1.0.0" or extract from folder metadata
- `[AUTHOR]` - Extract from folder metadata or use "AI Agent"
- `[DATE]` - Current date (YYYY-MM-DD)
- `[STATUS]` - "Production Ready" or extract from folder
- `[FRAMEWORK]` - Extract from folder content analysis
- `[PROJECT_NAME]` - Extract from folder name or metadata
- `[OUTPUT_EXPECTED]` - Describe what this package contains/generates
- `[EXECUTION_TIME]` - Estimate time to use this package

## Contextual Snippets Placeholders
- `[FILE_NAME]` - Actual filename from folder
- `[FILE_PURPOSE]` - First sentence or summary from file content
- `[KEYWORDS]` - Array of 3-10 keywords extracted from file
- `[TIER_ASSIGNMENT]` - 1, 2, or 3 based on file importance

## File Inventory Placeholders
- `[FILE_NAME]` - Actual filename
- `[FILE_PURPOSE]` - Specific, actionable purpose statement
- `[USE_WHEN]` - Scenario-based statement of when to use
- `[TIER_ASSIGNMENT]` - 1, 2, or 3
- `[WORD_COUNT]` - Actual word count from file analysis

## Content Placeholders
- `[FOLDER_DESCRIPTION]` - One sentence summary
- `[OVERVIEW_TEXT]` - 2-3 paragraphs from folder analysis
- `[CORE_PURPOSE]` - One sentence primary purpose
- `[KEY_OUTCOME]` - One sentence expected result
- `[KEY_CONCEPTS]` - 3-10 concepts from content analysis
- `[OUTCOMES]` - 3-5 outcomes from folder purpose
- `[TIER_X_FILES]` - List of files for each tier
- `[MAX_TOKENS]` - Calculate total if all files loaded
- `[SAVINGS_PERCENT]` - Calculate context savings percentage

## Document Guide Placeholders
- `[FILE_PURPOSE_SHORT]` - Brief purpose (for heading)
- `[CONTAINS]` - List of main content elements
- `[USE_WHEN_SCENARIO]` - Specific scenarios
- `[KEY_SECTIONS]` - Main sections in file
- `[TIER_DESCRIPTION]` - Description of tier (essential/core/reference)

## Notes
- Remove all placeholder text before delivery
- Remove all inline comments (lines starting with #)
- Ensure all placeholders are replaced with actual content
- Validate YAML syntax after replacement

---

**End of Template**

