---
title: Expert Framework Deployment Plan for tests/T01
date: 2025-12-24
status: Ready for Execution
classification: Implementation Guide
framework: expert-framework
purpose: Deploy minimal working test instance to tests/T01/
---

# Expert Framework Deployment Plan for tests/T01

**Objective:** Create a minimal working test instance of expert-framework in `tests/T01/` that demonstrates the framework structure and can run basic scaffolding operations.

**Date:** 2025-12-24  
**Source:** `tmp/test-scaffold-run-expert-framework/`  
**Target:** `tests/T01/`  
**Status:** Ready for execution

---

## 📋 Overview

### What is tests/T01?
A minimal test instance of the expert-framework that:
1. Demonstrates the complete directory structure
2. Runs scaffolding operations (scaffold_os.py, validate_scaffold.py)
3. Serves as integration test baseline
4. Validates framework design before production deployment

### What it's NOT
- ❌ Production deployment (no actual execution tools yet)
- ❌ Complete implementation (executions/ has README only)
- ❌ Knowledge base (shared-knowledgebase/ has manifest only)
- ❌ Tested agents (test/ directory is empty)

---

## 🎯 Success Criteria

### Must Have (Tier 1)
- ✅ Complete directory structure (agents/, directives/, executions/, etc.)
- ✅ Scaffold scripts work (scaffold_os.py, validate_scaffold.py)
- ✅ Core directives present (KB_GUARDRAILS.md, HANDOFF_PROTOCOL.md, etc.)
- ✅ Agent system-instructions files (7 agents)
- ✅ src/agentic_os/ module functional (paths.py, render.py, checks.py)

### Should Have (Tier 2)
- ⚠️ README.md explaining T01 purpose
- ⚠️ requirements.txt with Python dependencies
- ⚠️ .env.example template for API keys
- ⚠️ test_scaffold.py integration test script
- ⚠️ pyproject.toml for package metadata

### Nice to Have (Tier 3)
- ⚠️ Example execution tool (even if simple)
- ⚠️ Example knowledge base entry
- ⚠️ Example test case
- ⚠️ CI/CD integration script

---

## 📁 Files to Copy

### From tmp/test-scaffold-run-expert-framework/

#### 1. Core Source Code (Copy Entire)
```bash
# Library code
tests/T01/src/agentic_os/
├── __init__.py          # Package initialization
├── paths.py             # Canonical path definitions (2.4KB, 80 lines)
├── render.py            # Template rendering utilities (1.3KB, 45 lines)
├── checks.py            # Validation rules (4.9KB, 160 lines)
└── templates/           # Jinja2 templates (if any)

# Total: ~8.6KB, ~285 lines of Python
```

**Why:** Core library that all scaffolding operations depend on.

---

#### 2. Scaffold Scripts (Copy Entire)
```bash
tests/T01/scripts/
├── scaffold_os.py       # Main scaffold generator (~400 lines)
├── validate_scaffold.py # Structure validator (~200 lines)
└── rehome_drafts.py     # Artifact reorganization (~150 lines)

# Total: ~750 lines of Python
```

**Why:** Essential for creating and validating framework structure.

---

#### 3. Directives (Copy Entire)
```bash
tests/T01/directives/
├── README.md                    # Overview of all directives
├── KB_GUARDRAILS.md            # KB-first enforcement
├── HANDOFF_PROTOCOL.md          # State transfer rules
├── PROGRESSIVE_LOADING.md       # Context management
├── FAILURE_HANDLING.md          # Error handling
├── AGENT_HOOKS.md               # Hooks contract
└── templates/
    ├── plan.md                  # Planning template
    ├── build.md                 # Build template
    ├── self-improve.md          # Self-improvement template
    ├── plan_build_improve.md    # Combined workflow
    └── expertise.yaml.example   # Knowledge format example
```

**Why:** Core behavior contracts that agents must follow.

---

#### 4. Agents (Copy Structure + System Instructions)
```bash
tests/T01/agents/
├── metagpt/
│   ├── metagpt_system-instructions.md
│   ├── kb_metagpt-manifest.md
│   ├── mcp.json
│   ├── .env.example (NEW - create this)
│   └── [empty directories: directives/, eval/, executions/, sessions/, test/]
├── researchgpt/
│   ├── researchgpt_system-instructions.md
│   ├── kb_researchgpt-manifest.md
│   ├── mcp.json
│   ├── .env.example (NEW)
│   └── [empty directories]
├── analysisgpt/ [same pattern]
├── designgpt/ [same pattern]
├── implementationgpt/ [same pattern]
├── testgpt/ [same pattern]
└── evaluationgpt/ [same pattern]

# 7 agents × 4 files = 28 files
# + 7 agents × 5 empty directories = 35 directories
```

**Why:** Agent definitions are core to framework architecture.

---

#### 5. Executions (Copy README Only)
```bash
tests/T01/executions/
├── README.md            # Index of available tools
└── [empty directories: tools/, workflows/, utils/, eval/, hooks/]
```

**Why:** Structure placeholder - actual tools will be added later.

---

#### 6. Shared Knowledge Base (Copy Manifest Only)
```bash
tests/T01/shared-knowledgebase/
├── manifest.md          # Master index
├── README.md (NEW - create this)
└── [empty directories: expertise/, context/, references/, frameworks/, snippets/]
```

**Why:** Structure placeholder - knowledge will be added later.

---

#### 7. Empty Directories (Create Structure)
```bash
tests/T01/planning/      # Planning state machine files (empty)
tests/T01/sessions/      # Session logs (empty)
│   └── workflows/       # Workflow sessions (empty)
tests/T01/eval/          # Evaluation results (empty)
tests/T01/test/          # Tests & validation (empty)
tests/T01/logs/          # Audit logs (empty)
│   └── errors/          # Error forensics (empty)
```

**Why:** Required directories for framework operation.

---

### Files NOT to Copy

#### Provenance Files (Skip)
```bash
❌ marked-for-deletion/  # Provenance docs, not needed for tests
   ├── AGENTS.example.md
   ├── CONTEXT_ENGINEERING_UPDATE.md
   ├── DIRECTORY_STRUCTURE.md
   └── [9 other provenance files]
```

**Why:** Historical artifacts not needed for functional test.

---

#### System Files (Skip)
```bash
❌ .DS_Store             # macOS system file
❌ __pycache__/          # Python build artifacts
```

**Why:** System-generated, not part of framework.

---

## 📝 Files to Create (New)

### 1. tests/T01/README.md
```markdown
# Expert Framework - Test Instance T01

**Purpose:** Minimal working test instance demonstrating framework structure

**Status:** Scaffold Only (25% complete)  
**Created:** 2025-12-24

## What This Is
- Complete directory structure (✅)
- Scaffold scripts functional (✅)
- Core directives present (✅)
- Execution tools (❌ TODO)
- Knowledge base (❌ TODO)
- Tests (❌ TODO)

## Quick Start
```bash
cd tests/T01

# Validate structure
python scripts/validate_scaffold.py --verbose

# Re-generate if needed
python scripts/scaffold_os.py --apply --force
```

## Missing for Production
- Execution tools in `executions/tools/` (0/X files)
- Execution workflows in `executions/workflows/` (0/X files)
- Knowledge base content in `shared-knowledgebase/` (0/X entries)
- Integration tests in `test/` (0/X tests)
- Agent configurations in `agents/*/` (.env files need values)

## Next Steps
1. Create example execution tool
2. Populate knowledge base
3. Write integration tests
4. Deploy to `src/` when ready
```

---

### 2. tests/T01/requirements.txt
```txt
# Core dependencies
pyyaml>=6.0
jinja2>=3.1.0
pathspec>=0.11.0

# Optional dependencies (for execution tools)
httpx>=0.25.0
python-dotenv>=1.0.0

# Development dependencies
pytest>=7.0.0
ruff>=0.1.0
```

---

### 3. tests/T01/.env.example
```bash
# Expert Framework - Test Instance T01
# Copy this file to .env and fill in your values
# NEVER commit .env to git

# Project Configuration
PROJECT_ROOT="tests/T01"
PROJECT_NAME="expert-framework-test"
AGENT_NAME="test-agent"

# LLM Provider Configuration (for future execution tools)
ANTHROPIC_API_KEY="sk-ant-..."
OPENAI_API_KEY="sk-..."

# Optional Providers
GEMINI_API_KEY="..."
MOONSHOT_API_KEY="..."

# Constraints
MAX_COST_PER_REQUEST="0.50"      # USD
MAX_RETRIES="6"
RETRY_TIMEOUT_MINUTES="10"

# Features
ENABLE_THINKING_MODE="true"
ENABLE_KB_FIRST="true"
ENABLE_RULES_CHECKING="true"

# Logging
LOG_LEVEL="INFO"
LOG_TO_FILE="true"
AUDIT_LOG_ENABLED="true"
```

---

### 4. tests/T01/pyproject.toml
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "expert-framework-test-t01"
version = "0.1.0"
description = "Expert Framework - Test Instance T01"
requires-python = ">=3.11"
dependencies = [
    "pyyaml>=6.0",
    "jinja2>=3.1.0",
    "pathspec>=0.11.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "ruff>=0.1.0",
]

[tool.ruff]
line-length = 100
target-version = "py311"
```

---

### 5. tests/T01/test_scaffold.py
```python
#!/usr/bin/env python3
"""
Integration test for expert-framework scaffold.

Usage:
    python test_scaffold.py
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from agentic_os.paths import OSPaths
from agentic_os.checks import ScaffoldValidator


def test_structure():
    """Test that all required directories exist."""
    paths = OSPaths(Path(__file__).parent)
    
    required_dirs = [
        paths.root / "src" / "agentic_os",
        paths.root / "scripts",
        paths.root / "directives",
        paths.root / "agents",
        paths.root / "executions",
        paths.root / "shared-knowledgebase",
        paths.root / "planning",
        paths.root / "sessions",
        paths.root / "eval",
        paths.root / "test",
        paths.root / "logs",
    ]
    
    missing = [d for d in required_dirs if not d.exists()]
    
    if missing:
        print(f"❌ FAIL: Missing directories:")
        for d in missing:
            print(f"   - {d}")
        return False
    
    print("✅ PASS: All required directories exist")
    return True


def test_core_files():
    """Test that core files exist."""
    root = Path(__file__).parent
    
    required_files = [
        root / "src" / "agentic_os" / "__init__.py",
        root / "src" / "agentic_os" / "paths.py",
        root / "src" / "agentic_os" / "render.py",
        root / "src" / "agentic_os" / "checks.py",
        root / "scripts" / "scaffold_os.py",
        root / "scripts" / "validate_scaffold.py",
        root / "directives" / "README.md",
        root / "directives" / "KB_GUARDRAILS.md",
    ]
    
    missing = [f for f in required_files if not f.exists()]
    
    if missing:
        print(f"❌ FAIL: Missing core files:")
        for f in missing:
            print(f"   - {f}")
        return False
    
    print("✅ PASS: All core files exist")
    return True


def test_agents():
    """Test that all 7 agents exist with required files."""
    root = Path(__file__).parent
    agents_dir = root / "agents"
    
    required_agents = [
        "metagpt", "researchgpt", "analysisgpt", "designgpt",
        "implementationgpt", "testgpt", "evaluationgpt"
    ]
    
    missing_agents = []
    for agent in required_agents:
        agent_dir = agents_dir / agent
        if not agent_dir.exists():
            missing_agents.append(agent)
            continue
        
        # Check required files
        required_files = [
            agent_dir / f"{agent}_system-instructions.md",
            agent_dir / f"kb_{agent}-manifest.md",
            agent_dir / "mcp.json",
        ]
        
        for f in required_files:
            if not f.exists():
                missing_agents.append(f"{agent}/{f.name}")
    
    if missing_agents:
        print(f"❌ FAIL: Missing agents or agent files:")
        for item in missing_agents:
            print(f"   - {item}")
        return False
    
    print("✅ PASS: All 7 agents exist with required files")
    return True


def main():
    """Run all tests."""
    print("Expert Framework - Test Instance T01")
    print("=" * 50)
    print()
    
    tests = [
        ("Directory structure", test_structure),
        ("Core files", test_core_files),
        ("Agents", test_agents),
    ]
    
    results = []
    for name, test_func in tests:
        print(f"Testing: {name}...")
        result = test_func()
        results.append((name, result))
        print()
    
    # Summary
    print("=" * 50)
    print("Summary:")
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

---

## 🚀 Deployment Commands

### Step 1: Create tests/T01 Directory
```bash
cd /Volumes/uss/cloudworkspace/0_operator/1_Inbox/taskholder/th_agent-EXPERT-framework
mkdir -p tests/T01
```

### Step 2: Copy Files
```bash
# Copy source code
cp -r tmp/test-scaffold-run-expert-framework/src/ tests/T01/

# Copy scripts
cp -r tmp/test-scaffold-run-expert-framework/scripts/ tests/T01/

# Copy directives
cp -r tmp/test-scaffold-run-expert-framework/directives/ tests/T01/

# Copy agents
cp -r tmp/test-scaffold-run-expert-framework/agents/ tests/T01/

# Copy executions (README only)
mkdir -p tests/T01/executions
cp tmp/test-scaffold-run-expert-framework/executions/README.md tests/T01/executions/
mkdir -p tests/T01/executions/{tools,workflows,utils,eval,hooks}

# Copy shared-knowledgebase (manifest only)
mkdir -p tests/T01/shared-knowledgebase
cp tmp/test-scaffold-run-expert-framework/shared-knowledgebase/manifest.md tests/T01/shared-knowledgebase/
mkdir -p tests/T01/shared-knowledgebase/{expertise,context,references,frameworks,snippets}

# Create empty directories
mkdir -p tests/T01/planning
mkdir -p tests/T01/sessions/workflows
mkdir -p tests/T01/eval
mkdir -p tests/T01/test
mkdir -p tests/T01/logs/errors
```

### Step 3: Create New Files
```bash
# Create README.md (use content from above)
cat > tests/T01/README.md << 'EOF'
[Content from Section "1. tests/T01/README.md" above]
EOF

# Create requirements.txt (use content from above)
cat > tests/T01/requirements.txt << 'EOF'
[Content from Section "2. tests/T01/requirements.txt" above]
EOF

# Create .env.example (use content from above)
cat > tests/T01/.env.example << 'EOF'
[Content from Section "3. tests/T01/.env.example" above]
EOF

# Create pyproject.toml (use content from above)
cat > tests/T01/pyproject.toml << 'EOF'
[Content from Section "4. tests/T01/pyproject.toml" above]
EOF

# Create test_scaffold.py (use content from above)
cat > tests/T01/test_scaffold.py << 'EOF'
[Content from Section "5. tests/T01/test_scaffold.py" above]
EOF

chmod +x tests/T01/test_scaffold.py
```

### Step 4: Validate Deployment
```bash
cd tests/T01

# Test integration
python test_scaffold.py

# Validate scaffold
python scripts/validate_scaffold.py --verbose

# Expected output: All checks pass ✓
```

---

## 📊 File Count Summary

| Category | Files | Directories | Lines of Code |
|----------|-------|-------------|---------------|
| **Source Code** (src/) | 4 | 2 | ~285 |
| **Scripts** | 3 | 1 | ~750 |
| **Directives** | 11 | 2 | ~2000 (estimated) |
| **Agents** | 28 | 42 | ~1500 (estimated) |
| **Executions** | 1 (README) | 6 | ~50 |
| **Knowledge Base** | 1 (manifest) | 6 | ~100 |
| **Empty Dirs** | 0 | 8 | 0 |
| **New Files** | 5 | 0 | ~200 |
| **TOTAL** | **53** | **67** | **~4,885** |

---

## ✅ Validation Checklist

### Pre-Deployment
- [x] Source: tmp/test-scaffold-run-expert-framework/ exists
- [x] Target: tests/T01/ directory name confirmed
- [x] Files to copy identified (53 files)
- [x] Files to create identified (5 new files)
- [x] Files to skip identified (marked-for-deletion/, .DS_Store)

### Post-Deployment
- [ ] tests/T01/ directory created
- [ ] All 53 files copied successfully
- [ ] All 5 new files created
- [ ] All 67 directories exist
- [ ] test_scaffold.py passes all tests
- [ ] validate_scaffold.py passes all checks
- [ ] No .DS_Store or __pycache__ copied

---

## 🔄 Next Steps After Deployment

### Phase 1: Validate (1 hour)
1. Run `python test_scaffold.py` → All tests pass
2. Run `python scripts/validate_scaffold.py --verbose` → All checks pass
3. Inspect directory structure → Matches plan
4. Check file sizes → ~50-100KB total

### Phase 2: Document (1 hour)
5. Update root README.md → Reference tests/T01/
6. Create TESTING.md → Document test strategy
7. Update FRAMEWORK.md → Add tests/ section
8. Create .gitignore → Ignore .env, __pycache__, .DS_Store

### Phase 3: Extend (2-3 hours)
9. Create example execution tool → executions/tools/example.py
10. Add example knowledge entry → shared-knowledgebase/expertise/example.md
11. Write first integration test → test/test_integration.py
12. Document gaps → ROADMAP.md

### Phase 4: Production Prep (5-10 hours)
13. Implement missing execution tools → executions/tools/planning.py, etc.
14. Populate knowledge base → shared-knowledgebase/expertise/
15. Create comprehensive tests → test/
16. Deploy to src/ → Final production structure

---

## 📝 Known Limitations

### What's Missing
- ❌ **Execution tools:** executions/tools/ is empty
- ❌ **Execution workflows:** executions/workflows/ is empty
- ❌ **Execution utilities:** executions/utils/ is empty
- ❌ **Knowledge base:** shared-knowledgebase/ has only manifest
- ❌ **Tests:** test/ directory is empty
- ❌ **Agent configs:** .env files need actual values
- ❌ **Integration tests:** Only basic test_scaffold.py provided

### What Works
- ✅ **Directory structure:** Complete and validated
- ✅ **Scaffold scripts:** scaffold_os.py and validate_scaffold.py functional
- ✅ **Core directives:** 6 directives + 5 templates present
- ✅ **Agent definitions:** 7 agents with system-instructions and manifests
- ✅ **Source library:** src/agentic_os/ module functional

---

## 🎯 Success Metrics

### Deployment Success
- ✅ tests/T01/ created with 53 files and 67 directories
- ✅ test_scaffold.py passes all 3 tests
- ✅ validate_scaffold.py reports no errors
- ✅ Total size <200KB (scaffold only, no large dependencies)

### Functional Success
- ✅ Can regenerate structure: `python scripts/scaffold_os.py --apply`
- ✅ Can validate structure: `python scripts/validate_scaffold.py`
- ✅ Can run tests: `python test_scaffold.py`
- ⚠️ Cannot run agents (no execution tools yet)
- ⚠️ Cannot access knowledge (knowledge base empty)

---

## 📚 References

- **Source:** `tmp/test-scaffold-run-expert-framework/`
- **Framework Spec:** `FRAMEWORK.md`
- **Agent Catalog:** `AGENTS.md`
- **Deployment Checklist:** `FRAMEWORK-CHECKLIST.md`
- **Structure Analysis:** `ANALYSIS_REPOSITORY_STRUCTURE.md`

---

**Deployment Plan Status:** ✅ Ready for execution  
**Estimated Time:** 30 minutes (automated) + 1 hour (validation)  
**Next Action:** Execute deployment commands in Step 1-4

---

**Created:** 2025-12-24  
**Format:** Deployment plan following expert-framework standards  
**Framework Version:** 1.0
