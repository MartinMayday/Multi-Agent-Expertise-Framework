# Expert Framework - File Index

Quick reference guide to all files in the reverse-engineered Expert Framework.

## 📚 Documentation Files

### README.md
**Purpose:** Complete framework documentation  
**Contents:**
- Overview and core concepts
- Mental model (4 pillars)
- Directory structure
- Command invocation patterns
- File types and structures
- Best practices (correct vs wrong)
- Expertise file schema
- Agent patterns
- Self-improvement mechanism
- Integration guide

**Start here** for understanding the framework.

### DIRECTORY_STRUCTURE.md
**Purpose:** Complete directory structure reference  
**Contents:**
- Root structure diagram
- Directory descriptions
- File naming conventions
- Example structures
- Creating new domains guide
- File dependencies
- Validation checklist

**Use this** when setting up new domains or understanding file organization.

### AGENTS.example.md
**Purpose:** Agent configuration guide  
**Contents:**
- Agent structure and patterns
- Example agents (planner, meta-agent, domain experts)
- Agent patterns (delegation, meta, domain, orchestration)
- Best practices (correct vs wrong)
- Agent vs Command vs Skill comparison
- Creating new agents guide

**Use this** when creating or configuring agents.

### SUMMARY.md
**Purpose:** Overview of all generated files  
**Contents:**
- List of all files
- Framework components
- Key patterns
- Usage guide
- Success criteria

**Use this** for quick reference and navigation.

## 🔧 Command Templates

### plan.md
**Purpose:** Planning command template  
**Location:** `.claude/commands/experts/<domain>/plan.md`  
**Function:** Creates structured implementation plans using domain expertise  
**Key Sections:**
- Variables (USER_PROMPT, EXPERTISE_PATH)
- Instructions (read expertise, create plan)
- Workflow (read expertise → analyze → plan → validate → write)
- Report (plan path, summary, patterns used)

**Copy this** to create planning commands for new domains.

### build.md
**Purpose:** Building command template  
**Location:** `.claude/commands/experts/<domain>/build.md`  
**Function:** Implements code changes following a structured plan  
**Key Sections:**
- Variables (PLAN_PATH, EXPERTISE_PATH)
- Instructions (read plan, follow expertise, implement)
- Workflow (read plan → read expertise → implement → validate)
- Report (files created/modified, patterns followed)

**Copy this** to create building commands for new domains.

### self-improve.md
**Purpose:** Self-improvement command template  
**Location:** `.claude/commands/experts/<domain>/self-improve.md`  
**Function:** Validates and updates expertise based on codebase changes  
**Key Sections:**
- Variables (USER_PROMPT, CHECK_GIT_DIFF, FOCUS_AREA, EXPERTISE_PATH)
- Instructions (validate expertise, update if needed)
- Workflow (read expertise → validate → identify discrepancies → update)
- Report (validation findings, updates made)

**Copy this** to create self-improvement commands for new domains.

### plan_build_improve.md
**Purpose:** Chained workflow template  
**Location:** `.claude/commands/experts/<domain>/plan_build_improve.md`  
**Function:** Orchestrates complete implementation cycle  
**Key Sections:**
- Variables (USER_PROMPT, HUMAN_IN_THE_LOOP)
- Instructions (execute sequentially, use TaskOutput gates)
- Workflow (Step 1: Plan → Step 2: Build → Step 3: Self-Improve → Step 4: Report)
- Report (final workflow report path)

**Copy this** to create chained workflows for new domains.

## 📋 Configuration Files

### expertise.yaml.example
**Purpose:** Expertise file template  
**Location:** `.claude/commands/experts/<domain>/expertise.yaml`  
**Structure:**
- `information:` - Architecture, schemas, concepts
- `examples:` - Code snippets, use cases, real-world examples
- `patterns:` - Best practices, anti-patterns, workflows, common solutions
- `expertise:` - Decision guidelines, architectural principles, validation rules, troubleshooting

**Copy this** and populate with domain-specific knowledge.

## 🗂️ File Organization

### By Purpose

**Getting Started:**
1. Read `README.md` for framework overview
2. Read `DIRECTORY_STRUCTURE.md` for structure
3. Read `SUMMARY.md` for quick reference

**Creating Commands:**
1. Copy `plan.md` → `.claude/commands/experts/<domain>/plan.md`
2. Copy `build.md` → `.claude/commands/experts/<domain>/build.md`
3. Copy `self-improve.md` → `.claude/commands/experts/<domain>/self-improve.md`
4. Copy `plan_build_improve.md` → `.claude/commands/experts/<domain>/plan_build_improve.md`
5. Customize for your domain

**Creating Expertise:**
1. Copy `expertise.yaml.example` → `.claude/commands/experts/<domain>/expertise.yaml`
2. Populate with domain knowledge following four-pillar structure

**Creating Agents:**
1. Read `AGENTS.example.md` for patterns
2. Create `.claude/agents/<agent-name>.md`
3. Follow agent structure from examples

### By Workflow

**Question-Answering:**
- Use `question.md` pattern (from examples in codebase)
- Reference `expertise.yaml` for domain knowledge
- Validate against codebase

**Planning:**
- Use `plan.md` template
- Read `expertise.yaml` for patterns
- Create structured plan file

**Building:**
- Use `build.md` template
- Read plan file
- Follow expertise patterns
- Implement code changes

**Self-Improvement:**
- Use `self-improve.md` template
- Compare expertise to codebase
- Update expertise.yaml

**Complete Workflow:**
- Use `plan_build_improve.md` template
- Chain plan → build → self-improve
- Use Task/TaskOutput for sequential execution

## 🔍 Quick Reference

### Command Invocation
```
/experts:<domain>:<action> [arguments]
```

### Agent Invocation
```
@agent-<name> [prompt]
```

### File Locations
- Commands: `.claude/commands/experts/<domain>/<action>.md`
- Expertise: `.claude/commands/experts/<domain>/expertise.yaml`
- Agents: `.claude/agents/<agent-name>.md`
- Skills: `.claude/skills/<skill-name>.md`

### Mental Model (4 Pillars)
1. **Information** - Facts, schemas, concepts
2. **Examples** - Code snippets, use cases
3. **Patterns** - Best practices, workflows
4. **Expertise** - Decision guidelines, principles

## 📊 Analysis Files

### GAP_ANALYSIS.md
**Purpose:** Comprehensive gap analysis between originals and generated framework  
**Contents:**
- Original files analysis (what was incomplete)
- Generated files analysis (what was created)
- Gaps identified for production readiness
- Critical vs important vs nice-to-have gaps
- Production readiness checklist

**Use this** to understand what's missing for production and prioritize work.

### PRODUCTION_ROADMAP.md
**Purpose:** Roadmap from current state to production  
**Contents:**
- Phase 1: Alpha Testing (current)
- Phase 2: Beta (validation & testing)
- Phase 3: Production Readiness (operations)
- Phase 4: Advanced Features (post-launch)
- Implementation priorities
- Success metrics
- Timeline estimates

**Use this** to plan production deployment.

### VERIFICATION.md
**Purpose:** Verification that originals were used as references, not copied 1:1  
**Contents:**
- File-by-file verification
- Gap analysis summary
- Pattern extraction process
- Evidence of gap bridging
- Quantitative and qualitative analysis

**Use this** to verify framework was properly reverse-engineered.

## 📝 Notes

- All templates are based on patterns extracted from codebase examples
- No assumptions were made - all patterns come from provided files
- Original files were used as structural/conceptual references, not copied 1:1
- All gaps identified and filled based on patterns from complete examples
- Framework is conceptually complete and ready for alpha testing
- See GAP_ANALYSIS.md and PRODUCTION_ROADMAP.md for production readiness
- Customize templates for your specific domain needs
- Always validate expertise against codebase before trusting it

## 🚀 Next Steps

1. **Review** - Read README.md to understand framework
2. **Plan** - Choose a domain to start with
3. **Create** - Set up domain structure using templates
4. **Populate** - Fill expertise.yaml with domain knowledge
5. **Test** - Try question/plan/build workflows
6. **Iterate** - Refine based on usage

---

**All files located in:** `tmp/reverse-engineer-expert-framework/`

