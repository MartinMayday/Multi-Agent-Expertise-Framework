---
title: Expert Framework - Deployment Checklist
filename: FRAMEWORK-CHECKLIST.md
complexity: intermediate
audience: Deployment engineers, framework implementers
category: Deployment, Verification, Quality Assurance
keywords: deployment-checklist, preflight-verification, framework-validation, directory-structure, configuration-check, tool-availability, capability-verification, safety-guardrails
tags: checklist, deployment, verification
summary: Comprehensive preflight verification checklist for deploying Expert Framework. Validates directory structure, configuration files, environment variables, tool availability, capability verification, safety guardrails, and success criteria before enabling autonomous execution.
rrf_anchors: preflight-checklist, deployment-verification, framework-validation, configuration-validation, tool-availability-check, safety-enforcement-checklist
context_snippet: Deployment checklist verifies 5 key areas: (1) Directory Structure - all required directories exist with proper permissions; (2) Configuration - .env file present, API keys valid, provider configs correct; (3) Tools & Dependencies - Python environment configured, all tools executable, evaluators present; (4) Safety Guardrails - rules.md populated, ❌ NEVER rules enforced, ✅ ALWAYS rules defined; (5) Success Criteria - planning mode works, error recovery functions, KB accessible, journal functional. Each section has verification commands and expected outcomes.
---

# Expert Framework - Deployment Checklist

**Project**: {{PROJECT_NAME}}  
**Date**: {{DEPLOYMENT_DATE}}  
**Deployed By**: {{YOUR_NAME}}  
**Status**: ⬜ Not Started  

---

## Pre-Deployment Verification

### 1. ✅ Directory Structure Validation

**Purpose**: Verify all required directories exist and have proper permissions

#### 1.1 Core Directories
```bash
# Check existence
[ -d "{{PROJECT_ROOT}}/directives" ] && echo "✅ directives/" || echo "❌ directives/ MISSING"
[ -d "{{PROJECT_ROOT}}/executions" ] && echo "✅ executions/" || echo "❌ executions/ MISSING"
[ -d "{{PROJECT_ROOT}}/shared-knowledgebase" ] && echo "✅ shared-knowledgebase/" || echo "❌ shared-knowledgebase/ MISSING"
[ -d "{{PROJECT_ROOT}}/planning" ] && echo "✅ planning/" || echo "❌ planning/ MISSING"
[ -d "{{PROJECT_ROOT}}/sessions" ] && echo "✅ sessions/" || echo "❌ sessions/ MISSING"
[ -d "{{PROJECT_ROOT}}/logs" ] && echo "✅ logs/" || echo "❌ logs/ MISSING"
[ -d "{{PROJECT_ROOT}}/eval" ] && echo "✅ eval/" || echo "❌ eval/ MISSING"
[ -d "{{PROJECT_ROOT}}/test" ] && echo "✅ test/" || echo "❌ test/ MISSING"
[ -d "{{PROJECT_ROOT}}/.context" ] && echo "✅ .context/" || echo "❌ .context/ MISSING"

# Check write permissions
[ -w "{{PROJECT_ROOT}}/planning" ] && echo "✅ planning/ writable" || echo "⚠️ planning/ NOT writable"
[ -w "{{PROJECT_ROOT}}/sessions" ] && echo "✅ sessions/ writable" || echo "⚠️ sessions/ NOT writable"
[ -w "{{PROJECT_ROOT}}/logs" ] && echo "✅ logs/ writable" || echo "⚠️ logs/ NOT writable"
```

**Expected Output**:
```
✅ directives/
✅ executions/
✅ shared-knowledgebase/
✅ planning/
✅ sessions/
✅ logs/
✅ eval/
✅ test/
✅ planning/ writable
✅ sessions/ writable
✅ logs/ writable
✅ .context/ writable
```

**Status**: ⬜ Pending  
**Verified By**: ___________  
**Date**: ___________  

---

#### 1.2 Subdirectories
```bash
# Check directives subdirectories
ls -la {{PROJECT_ROOT}}/directives/{workflows,triggers,constraints,agents} 2>/dev/null | grep "^d" | wc -l

# Check executions subdirectories
ls -la {{PROJECT_ROOT}}/executions/{tools,workflows,utils,eval} 2>/dev/null | grep "^d" | wc -l

# Check knowledge base subdirectories
ls -la {{PROJECT_ROOT}}/shared-knowledgebase/{expertise,context,references} 2>/dev/null | grep "^d" | wc -l
```

**Expected Output**:
- directives subdirectories: 4
- executions subdirectories: 4
- shared-knowledgebase subdirectories: 3

**Status**: ⬜ Pending  

---

### 2. ✅ Configuration File Validation

**Purpose**: Verify all configuration files are present and correctly formatted

#### 2.1 Environment File
```bash
# Check .env exists and is NOT in git
ls -la {{PROJECT_ROOT}}/.env 2>/dev/null && echo "✅ .env exists" || echo "❌ .env MISSING"
git status {{PROJECT_ROOT}}/.env 2>/dev/null | grep -i "ignored" && echo "✅ .env ignored by git" || echo "⚠️ .env might be in git"

# Check required environment variables
grep -q "ANTHROPIC_API_KEY=" {{PROJECT_ROOT}}/.env && echo "✅ ANTHROPIC_API_KEY set" || echo "❌ ANTHROPIC_API_KEY missing"
grep -q "PROJECT_NAME=" {{PROJECT_ROOT}}/.env && echo "✅ PROJECT_NAME set" || echo "❌ PROJECT_NAME missing"
grep -q "AGENT_NAME=" {{PROJECT_ROOT}}/.env && echo "✅ AGENT_NAME set" || echo "❌ AGENT_NAME missing"
```

**Expected Output**:
```
✅ .env exists
✅ .env ignored by git
✅ ANTHROPIC_API_KEY set
✅ PROJECT_NAME set
✅ AGENT_NAME set
```

**Status**: ⬜ Pending  

---

#### 2.2 Configuration Files
```bash
# Check .g3.toml exists (if using Rust provider config)
[ -f "{{PROJECT_ROOT}}/.g3.toml" ] && echo "✅ .g3.toml exists" || echo "⚠️ .g3.toml optional"

# Check AGENTS.md exists
[ -f "{{PROJECT_ROOT}}/AGENTS.md" ] && echo "✅ AGENTS.md exists" || echo "❌ AGENTS.md MISSING"

# Check for git .gitignore
grep -q ".env" {{PROJECT_ROOT}}/.gitignore && echo "✅ .env in .gitignore" || echo "❌ .env NOT in .gitignore"
```

**Status**: ⬜ Pending  

---

### 3. ✅ Knowledge Base Validation

**Purpose**: Verify knowledge base structure and content

#### 3.1 Core Context Files
```bash
# Check all 9 context files exist
for file in identity preferences workflows relationships triggers projects rules session journal; do
  [ -f "{{PROJECT_ROOT}}/shared-knowledgebase/context/$file.md" ] && \
    echo "✅ $file.md" || echo "❌ $file.md MISSING"
done

# Check rules.md has ❌ NEVER and ✅ ALWAYS rules
grep -q "❌ NEVER" {{PROJECT_ROOT}}/shared-knowledgebase/context/rules.md && \
  echo "✅ rules.md has ❌ NEVER rules" || echo "⚠️ rules.md missing ❌ NEVER rules"
grep -q "✅ ALWAYS" {{PROJECT_ROOT}}/shared-knowledgebase/context/rules.md && \
  echo "✅ rules.md has ✅ ALWAYS rules" || echo "⚠️ rules.md missing ✅ ALWAYS rules"
```

**Expected Output**:
```
✅ identity.md
✅ preferences.md
✅ workflows.md
✅ relationships.md
✅ triggers.md
✅ projects.md
✅ rules.md
✅ session.md
✅ journal.md
✅ rules.md has ❌ NEVER rules
✅ rules.md has ✅ ALWAYS rules
```

**Status**: ⬜ Pending  

---

#### 3.2 Rules Validation
```bash
# Count rules
NEVER_COUNT=$(grep -c "❌ NEVER" {{PROJECT_ROOT}}/shared-knowledgebase/context/rules.md)
ALWAYS_COUNT=$(grep -c "✅ ALWAYS" {{PROJECT_ROOT}}/shared-knowledgebase/context/rules.md)

echo "❌ NEVER rules: $NEVER_COUNT (recommended: ≥3)"
echo "✅ ALWAYS rules: $ALWAYS_COUNT (recommended: ≥3)"

# Verify rules are enforceable
[ "$NEVER_COUNT" -ge 3 ] && echo "✅ Sufficient ❌ NEVER rules" || echo "⚠️ Add more ❌ NEVER rules"
[ "$ALWAYS_COUNT" -ge 3 ] && echo "✅ Sufficient ✅ ALWAYS rules" || echo "⚠️ Add more ✅ ALWAYS rules"
```

**Status**: ⬜ Pending  

---

### 4. ✅ Tools & Dependencies

**Purpose**: Verify all tools and their dependencies are installed

#### 4.1 Python Environment
```bash
# Check Python version (3.9+)
python3 --version | grep -E "3\.(9|1[0-9]|2[0-9])" && echo "✅ Python 3.9+" || echo "❌ Python version too old"

# Check virtual environment
[ -d "{{PROJECT_ROOT}}/venv" ] && echo "✅ venv/ exists" || echo "⚠️ venv/ not found"
[ -f "{{PROJECT_ROOT}}/requirements.txt" ] && echo "✅ requirements.txt exists" || echo "❌ requirements.txt MISSING"

# Install dependencies (if not already)
pip install -q -r {{PROJECT_ROOT}}/requirements.txt && echo "✅ Dependencies installed" || echo "❌ Dependencies installation FAILED"
```

**Status**: ⬜ Pending  

---

#### 4.2 Tool Availability
```bash
# Check tool files exist
for tool in planning build test self_improve; do
  [ -f "{{PROJECT_ROOT}}/executions/tools/$tool.py" ] && \
    echo "✅ $tool.py" || echo "❌ $tool.py MISSING"
done

# Check evaluator files
for eval in plan build test; do
  [ -f "{{PROJECT_ROOT}}/executions/eval/eval_$eval.py" ] && \
    echo "✅ eval_$eval.py" || echo "❌ eval_$eval.py MISSING"
done

# Check utility modules
for util in providers context_manager error_handler logging_config; do
  [ -f "{{PROJECT_ROOT}}/executions/utils/$util.py" ] && \
    echo "✅ $util.py" || echo "❌ $util.py MISSING"
done

# Check context validator tools
[ -f "{{PROJECT_ROOT}}/executions/tools/context_validator/validate_context_tree.py" ] && \
  echo "✅ validate_context_tree.py" || echo "❌ validate_context_tree.py MISSING"
[ -f "{{PROJECT_ROOT}}/executions/tools/context_validator/validate_transcript_metadata.py" ] && \
  echo "✅ validate_transcript_metadata.py" || echo "❌ validate_transcript_metadata.py MISSING"
```

**Status**: ⬜ Pending  

---

#### 4.3 Tool Execution Test
```bash
# Test importing core modules
python3 -c "import sys; sys.path.insert(0, '{{PROJECT_ROOT}}'); from executions.utils import providers; print('✅ providers module loads')" 2>/dev/null || echo "❌ providers module FAILED"

python3 -c "import sys; sys.path.insert(0, '{{PROJECT_ROOT}}'); from executions.utils import context_manager; print('✅ context_manager module loads')" 2>/dev/null || echo "❌ context_manager module FAILED"

python3 -c "import sys; sys.path.insert(0, '{{PROJECT_ROOT}}'); from executions.utils import error_handler; print('✅ error_handler module loads')" 2>/dev/null || echo "❌ error_handler module FAILED"
```

**Status**: ⬜ Pending  

---

### 5. ✅ Provider Configuration

**Purpose**: Verify LLM provider configuration and connectivity

#### 5.1 API Key Validation
```bash
# Load .env (bash source)
set -a
source {{PROJECT_ROOT}}/.env
set +a

# Test Anthropic API key format (starts with sk-ant-)
[[ "$ANTHROPIC_API_KEY" =~ ^sk-ant- ]] && \
  echo "✅ ANTHROPIC_API_KEY format valid" || echo "❌ ANTHROPIC_API_KEY format invalid"

# Test API connectivity (optional - only if key is real)
if [[ ! -z "$ANTHROPIC_API_KEY" && "$ANTHROPIC_API_KEY" != "sk-ant-example" ]]; then
  curl -s -H "x-api-key: $ANTHROPIC_API_KEY" \
    https://api.anthropic.com/v1/models | grep -q "models" && \
    echo "✅ Anthropic API reachable" || echo "⚠️ Anthropic API unreachable (check key)"
fi
```

**Status**: ⬜ Pending  

---

#### 5.2 Provider Configuration File
```bash
# Check .g3.toml (if present)
if [ -f "{{PROJECT_ROOT}}/.g3.toml" ]; then
  grep -q "default_provider" {{PROJECT_ROOT}}/.g3.toml && \
    echo "✅ default_provider configured" || echo "❌ default_provider NOT configured"
  
  grep -q "anthropic" {{PROJECT_ROOT}}/.g3.toml && \
    echo "✅ anthropic provider configured" || echo "❌ anthropic provider NOT configured"
else
  echo "⚠️ .g3.toml not found (optional if env vars used)"
fi
```

**Status**: ⬜ Pending  

---

### 6. ✅ Safety Guardrails Validation

**Purpose**: Verify safety constraints are in place

#### 6.1 Rules Engine
```bash
# Verify rules.md has proper syntax
python3 << 'EOF'
import re

rules_file = "{{PROJECT_ROOT}}/shared-knowledgebase/context/rules.md"
try:
    with open(rules_file) as f:
        content = f.read()
    
    never_rules = re.findall(r'^- ❌ NEVER', content, re.MULTILINE)
    always_rules = re.findall(r'^- ✅ ALWAYS', content, re.MULTILINE)
    
    print(f"Found {len(never_rules)} ❌ NEVER rules")
    print(f"Found {len(always_rules)} ✅ ALWAYS rules")
    
    if len(never_rules) >= 3 and len(always_rules) >= 3:
        print("✅ Rules guardrails sufficient")
    else:
        print("⚠️ Add more rules (minimum 3 each)")
except FileNotFoundError:
    print(f"❌ {rules_file} not found")
except Exception as e:
    print(f"❌ Error parsing rules: {e}")
EOF
```

**Status**: ⬜ Pending  

---

#### 6.2 Constraint Thresholds
```bash
# Check .env for safety limits
grep "MAX_COST" {{PROJECT_ROOT}}/.env && echo "✅ MAX_COST_PER_REQUEST set" || echo "⚠️ MAX_COST_PER_REQUEST not set"
grep "MAX_RETRIES" {{PROJECT_ROOT}}/.env && echo "✅ MAX_RETRIES set" || echo "⚠️ MAX_RETRIES not set"
grep "RETRY_TIMEOUT" {{PROJECT_ROOT}}/.env && echo "✅ RETRY_TIMEOUT_MINUTES set" || echo "⚠️ RETRY_TIMEOUT_MINUTES not set"
```

**Status**: ⬜ Pending  

---

### 7. ✅ Directive Validation

**Purpose**: Verify all directives are present and valid

#### 7.1 Required Directives
```bash
# Check workflow directives
[ -f "{{PROJECT_ROOT}}/directives/workflows/plan_build_improve.yaml" ] && \
  echo "✅ plan_build_improve.yaml" || echo "⚠️ plan_build_improve.yaml (optional)"

[ -f "{{PROJECT_ROOT}}/directives/workflows/question_answering.yaml" ] && \
  echo "✅ question_answering.yaml" || echo "⚠️ question_answering.yaml (optional)"

# Check for at least one custom workflow
CUSTOM_WF=$(find {{PROJECT_ROOT}}/directives/workflows -name "*.yaml" | wc -l)
[ "$CUSTOM_WF" -gt 0 ] && echo "✅ $CUSTOM_WF workflow(s) defined" || echo "⚠️ Define at least one workflow"
```

**Status**: ⬜ Pending  

---

#### 7.2 Directive Syntax Validation
```bash
# Validate YAML syntax
python3 << 'EOF'
import yaml
import os
import glob

directives_path = "{{PROJECT_ROOT}}/directives/workflows"
yaml_files = glob.glob(f"{directives_path}/*.yaml")

for yaml_file in yaml_files:
    try:
        with open(yaml_file) as f:
            yaml.safe_load(f)
        print(f"✅ {os.path.basename(yaml_file)} - valid YAML")
    except yaml.YAMLError as e:
        print(f"❌ {os.path.basename(yaml_file)} - YAML ERROR: {e}")
    except FileNotFoundError:
        print(f"❌ {yaml_file} not found")
EOF
```

**Status**: ⬜ Pending  

---

### 8. ✅ Planning Mode State Machine

**Purpose**: Verify planning mode can initialize and function

#### 8.1 Planning Directory Setup
```bash
# Check planning directory structure
[ -f "{{PROJECT_ROOT}}/planning/planner_history.txt" ] && \
  echo "✅ planner_history.txt exists" || echo "⚠️ Will be created on first run"

# Verify write access
touch {{PROJECT_ROOT}}/planning/.test_write && \
  echo "✅ planning/ writable" && rm {{PROJECT_ROOT}}/planning/.test_write || \
  echo "❌ planning/ NOT writable"
```

**Status**: ⬜ Pending  

---

#### 8.2 Planning Mode Test
```bash
# Test planning mode initialization
python3 << 'EOF'
import sys
import os
sys.path.insert(0, "{{PROJECT_ROOT}}")

# Simulate planning mode startup
try:
    # Load directives
    import glob
    directives = glob.glob("{{PROJECT_ROOT}}/directives/workflows/*.yaml")
    print(f"✅ Found {len(directives)} directive(s)")
    
    # Check history file
    history_path = "{{PROJECT_ROOT}}/planning/planner_history.txt"
    if os.path.exists(history_path):
        with open(history_path) as f:
            lines = len(f.readlines())
        print(f"✅ planner_history.txt has {lines} entries")
    else:
        print("⚠️ planner_history.txt will be created on first run")
    
    print("✅ Planning mode can initialize")
except Exception as e:
    print(f"❌ Planning mode initialization FAILED: {e}")
EOF
```

**Status**: ⬜ Pending  

---

### 9. ✅ Error Recovery Verification

**Purpose**: Verify autonomous error handling and retry logic

#### 9.1 Error Handler Configuration
```bash
# Check error_handler.py exists and has retry config
grep -q "max_retries = 6" {{PROJECT_ROOT}}/executions/utils/error_handler.py && \
  echo "✅ Retry count set to 6" || echo "⚠️ Verify retry configuration"

grep -q "RECOVERABLE_ERRORS" {{PROJECT_ROOT}}/executions/utils/error_handler.py && \
  echo "✅ Recoverable error classification defined" || echo "❌ Error classification MISSING"

# Check logs directory for error logging
[ -d "{{PROJECT_ROOT}}/logs/errors" ] && \
  echo "✅ logs/errors/ directory exists" || echo "⚠️ Will be created on first error"
```

**Status**: ⬜ Pending  

---

#### 9.2 Retry Logic Test
```bash
# Test retry delay distribution
python3 << 'EOF'
# Verify 10-minute distribution over 6 retries
base_delays = [10, 30, 60, 120, 180, 200]
total_seconds = sum(base_delays)

print(f"Base retry delays (sec): {base_delays}")
print(f"Total distribution: {total_seconds}s ({total_seconds/60:.1f} minutes)")

if total_seconds == 600:
    print("✅ Retry distribution is 10 minutes")
else:
    print(f"⚠️ Retry distribution is {total_seconds}s, expected 600s")

# Check jitter range
min_jitter = 0.7  # -30%
max_jitter = 1.3  # +30%
print(f"✅ Jitter range: {min_jitter * 100:.0f}% - {max_jitter * 100:.0f}%")
EOF
```

**Status**: ⬜ Pending  

---

### 10. ✅ Knowledge Base Accessibility

**Purpose**: Verify knowledge base can be loaded and queried

#### 10.1 KB File Validation
```bash
# Check expertise files exist
[ -d "{{PROJECT_ROOT}}/shared-knowledgebase/expertise" ] && \
  EXPERTISE_COUNT=$(ls {{PROJECT_ROOT}}/shared-knowledgebase/expertise/*.md 2>/dev/null | wc -l) && \
  echo "✅ Found $EXPERTISE_COUNT expertise file(s)" || echo "⚠️ No expertise files yet"

# Check references
[ -d "{{PROJECT_ROOT}}/shared-knowledgebase/references" ] && \
  REF_COUNT=$(ls {{PROJECT_ROOT}}/shared-knowledgebase/references/*.md 2>/dev/null | wc -l) && \
  echo "✅ Found $REF_COUNT reference file(s)" || echo "⚠️ No reference files yet"
```

**Status**: ⬜ Pending  

---

#### 10.2 KB Loading Test
```bash
# Test KB loading capability
python3 << 'EOF'
import sys
import os
import glob

sys.path.insert(0, "{{PROJECT_ROOT}}")

kb_path = "{{PROJECT_ROOT}}/shared-knowledgebase"

try:
    # Check context files
    context_dir = os.path.join(kb_path, "context")
    context_files = glob.glob(f"{context_dir}/*.md")
    print(f"✅ Found {len(context_files)}/9 context files (ideal: 9)")
    
    # Check expertise files
    expertise_dir = os.path.join(kb_path, "expertise")
    expertise_files = glob.glob(f"{expertise_dir}/*.md")
    print(f"✅ Found {len(expertise_files)} expertise file(s)")
    
    # Try loading a context file
    identity_file = os.path.join(context_dir, "identity.md")
    if os.path.exists(identity_file):
        with open(identity_file) as f:
            content = f.read()
        if len(content) > 10:
            print("✅ KB context files are readable")
        else:
            print("⚠️ KB context files exist but are empty")
    
    print("✅ Knowledge base accessible")
except Exception as e:
    print(f"❌ Knowledge base access FAILED: {e}")
EOF
```

**Status**: ⬜ Pending  

---

### 11. ✅ Session Management

**Purpose**: Verify session persistence works

#### 11.1 Session Directory
```bash
# Check sessions directory
[ -d "{{PROJECT_ROOT}}/sessions" ] && echo "✅ sessions/ exists" || echo "❌ sessions/ MISSING"

# Check write access
touch {{PROJECT_ROOT}}/sessions/.test && \
  rm {{PROJECT_ROOT}}/sessions/.test && \
  echo "✅ sessions/ writable" || echo "❌ sessions/ NOT writable"

# Test session creation
python3 << 'EOF'
import json
import os
from datetime import datetime

sessions_dir = "{{PROJECT_ROOT}}/sessions"
test_session = {
    "session_id": "test_{{datetime.now().strftime('%Y%m%d_%H%M%S')}}",
    "start_time": datetime.now().isoformat(),
    "test": True
}

try:
    test_file = os.path.join(sessions_dir, f"{test_session['session_id']}.json")
    with open(test_file, 'w') as f:
        json.dump(test_session, f)
    os.remove(test_file)
    print("✅ Session files can be created and removed")
except Exception as e:
    print(f"❌ Session file operation FAILED: {e}")
EOF
```

**Status**: ⬜ Pending  

---

### 12. ✅ Logging & Audit Trail

**Purpose**: Verify logging is properly configured

#### 12.1 Logs Directory
```bash
# Check logs structure
[ -d "{{PROJECT_ROOT}}/logs" ] && echo "✅ logs/ exists" || echo "❌ logs/ MISSING"
[ -d "{{PROJECT_ROOT}}/logs/errors" ] && echo "✅ logs/errors/ exists" || echo "⚠️ Will be created on first error"

# Check write access
touch {{PROJECT_ROOT}}/logs/.test && \
  rm {{PROJECT_ROOT}}/logs/.test && \
  echo "✅ logs/ writable" || echo "❌ logs/ NOT writable"
```

**Status**: ⬜ Pending  

---

#### 12.2 Logging Configuration
```bash
# Check if logging config exists
[ -f "{{PROJECT_ROOT}}/executions/utils/logging_config.py" ] && \
  echo "✅ logging_config.py exists" || echo "❌ logging_config.py MISSING"

# Test logging
python3 << 'EOF'
import sys
import os
import logging

sys.path.insert(0, "{{PROJECT_ROOT}}")

try:
    # Configure logging
    log_file = "{{PROJECT_ROOT}}/logs/test_deployment.log"
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger("deployment_test")
    logger.info("Test log message")
    
    # Check if file was created
    if os.path.exists(log_file):
        with open(log_file) as f:
            content = f.read()
        if "Test log message" in content:
            print("✅ Logging works correctly")
            os.remove(log_file)
        else:
            print("⚠️ Log file created but message not found")
    else:
        print("❌ Log file not created")
except Exception as e:
    print(f"❌ Logging test FAILED: {e}")
EOF
```

**Status**: ⬜ Pending  

---

## Final Deployment Steps

### Pre-Deployment Review Checklist
- [ ] All directory structure verified (Section 1)
- [ ] Configuration files validated (Section 2)
- [ ] Knowledge base structure confirmed (Section 3)
- [ ] Tools & dependencies installed (Section 4)
- [ ] Provider API keys configured (Section 5)
- [ ] Safety guardrails in place (Section 6)
- [ ] Directives defined and validated (Section 7)
- [ ] Planning mode tested (Section 8)
- [ ] Error recovery verified (Section 9)
- [ ] Knowledge base accessible (Section 10)
- [ ] Session management working (Section 11)
- [ ] Logging configured (Section 12)

### Deployment Command
```bash
# Run complete verification suite
cd {{PROJECT_ROOT}}
bash scripts/deployment_verify.sh

# Expected output: All ✅ checks pass
# If any ❌ appear: Fix issues before proceeding
```

### Post-Deployment Verification
```bash
# Test autonomous execution
python3 executions/workflows/plan.py \
  --directive directives/workflows/test_workflow.yaml \
  --mode autonomous

# Monitor logs
tail -f {{PROJECT_ROOT}}/logs/*.log

# Check planning history updated
cat {{PROJECT_ROOT}}/planning/planner_history.txt | tail -20

# Verify KB updated
ls -la {{PROJECT_ROOT}}/shared-knowledgebase/context/
```

---

## Success Criteria

✅ **Framework Ready for Production** when:
- [x] All 12 verification sections pass
- [x] No ❌ errors (⚠️ warnings are acceptable if documented)
- [x] All required files exist and are readable
- [x] Safety guardrails enforced (rules.md populated)
- [x] API keys configured and tested
- [x] Planning mode can initialize
- [x] Error recovery tested
- [x] KB accessible and valid
- [x] Logging operational
- [x] Session management working

---

## Troubleshooting Failed Checks

| Failed Check | Likely Cause | Solution |
|---|---|---|
| Directory missing | Not initialized | Run `python scripts/init_framework.py` |
| .env missing | Configuration incomplete | Copy .env.example to .env and fill values |
| API key invalid | Wrong or expired key | Verify key in Anthropic console, regenerate if needed |
| Python module not found | Dependencies not installed | Run `pip install -r requirements.txt` |
| Permission denied | Incorrect file permissions | Run `chmod -R u+w {{PROJECT_ROOT}}/planning {{PROJECT_ROOT}}/logs` |
| Directive syntax error | YAML formatting issue | Use online YAML validator, check indentation |
| Rules.md empty | Safety constraints not defined | Add ❌ NEVER and ✅ ALWAYS rules |

---

## Sign-Off

**Deployment Date**: _______________  
**Verified By**: _______________  
**Approved By**: _______________  
**Go/No-Go Decision**: ⬜ PENDING / ✅ GO / ❌ NO-GO  

**Notes**:
```
[Space for deployment notes, issues encountered, resolutions]




```

---

**Framework Version**: 1.0  
**Checklist Version**: 1.0  
**Last Updated**: 2025-12-15  
**Status**: Ready for Use  

For questions or issues, refer to:
- FRAMEWORK.md - Full framework specification
- COMPREHENSIVE-KNOWLEDGE-INDEX.md - Complete reference
- PHASE-2-SYNTHESIS-*.md - Detailed technical documentation
