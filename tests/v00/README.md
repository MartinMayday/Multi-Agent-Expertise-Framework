# tests/v00 - Framework Test Suite

## Overview

This directory contains integration tests for the **v00 Multi-Agent Expertise Framework**. It tests the core systems that were implemented in the remediation:

✓ Scaffold generation (DOE directory structure)  
✓ Context management (global + project rules)  
✓ Memory operations system (event logging, fact extraction, pattern recognition)  
✓ Multi-agent framework stubs  

## What's Here

```
tests/v00/
├── .context/                    # Test environment using actual Memory Ops structure
│   ├── 00_rules/               # Immutable test rules and conventions
│   ├── 01_state/               # Operational state (task queue, active session)
│   ├── 02_memory/              # Learning layer (decisions, patterns, entities)
│   └── 03_archive/             # Session logs and history
│
├── integration/                 # Integration test scripts
│   ├── test_scaffold.py         # Validate directory structure
│   ├── test_context_manager.py  # Context loading and merging
│   ├── test_memory_ops.py       # Event logging, fact extraction, patterns
│   └── test_agents.py           # Multi-agent framework stubs
│
└── README.md                    # This file
```

## Quick Start

### 1. View Test Setup
```bash
# Explore the test environment
ls -la tests/v00/.context/

# Check what tests are planned
cat tests/v00/.context/01_state/task_queue.json

# Review test rules
cat tests/v00/.context/00_rules/project.md
```

### 2. Run Tests (When Implemented)
```bash
cd tests/v00
python -m pytest integration/ -v
```

### 3. Check Results
```bash
# View test results
cat .context/01_state/active_session.json

# Check for detected patterns
cat .context/02_memory/patterns.md

# Review decisions made during testing
cat .context/02_memory/decisions.log.md
```

## Test Structure

### .context/ Directory - Real Test Harness

The `.context/` directory is **not** just test configuration—it's the actual Memory Operations System being tested. This enables:

1. **Structural Validation**: Tests verify all required subdirectories exist and have correct files
2. **Functional Testing**: Real ContextManager, EventLogger, etc. work against actual files
3. **Self-Learning**: PatternRecognizer analyzes real test execution to detect issues
4. **Traceability**: All test decisions recorded in `.context/02_memory/decisions.log.md`

### Test Layers

#### Layer 0: Scaffold Validation (00_rules)
- Verify project.md exists and is valid YAML/Markdown
- Verify style_guide.md covers Python conventions
- Verify team.md defines roles and communication

**Expected to Pass**: ✓ Yes - files created with correct structure

#### Layer 1: State Management (01_state)
- Verify active_session.json loads and validates against schema
- Verify task_queue.json has valid task structure
- Verify scratchpad.md is readable Markdown

**Expected to Pass**: ✓ Yes - files created with correct structure

#### Layer 2: Memory Operations (02_memory)
- Verify decisions.log.md follows ADR template
- Verify patterns.md has correct format
- Verify entities.json parses as valid JSON

**Expected to Pass**: ✓ Yes - files created with correct structure

#### Layer 3: Archive & Learning (03_archive)
- Verify sessions/ directory exists and is writable
- Verify .gitkeep file exists to ensure Git tracks directory

**Expected to Pass**: ✓ Yes - directory created with .gitkeep

## Integration Tests (Planned)

### test_scaffold.py
Tests that the scaffold system creates proper DOE structure:
```python
def test_scaffold_creates_all_layers():
    # Verify 0_directives, 1_orchestration, 2_executions exist
    
def test_context_structure_matches_plan():
    # Verify .context/ has all required subdirs and files
    
def test_rules_layer_readable():
    # Load and parse all 00_rules/* files
```

### test_context_manager.py
Tests context loading and rule merging:
```python
def test_load_project_rules():
    # Load 00_rules/ from .context/
    
def test_merge_global_and_project_rules():
    # Simulate merging ~/.expert-framework/ with .context/
    
def test_context_validation():
    # Verify loaded context matches schema
```

### test_memory_ops.py
Tests the complete Memory Operations System:
```python
def test_event_logger_ndjson_append():
    # Write events, verify NDJSON format
    
def test_fact_extractor_triplets():
    # Extract facts from sample logs
    
def test_pattern_recognizer_detection():
    # Detect repeated patterns in logs
    
def test_reflector_integration():
    # End-to-end session analysis
```

### test_agents.py
Tests multi-agent framework stubs:
```python
def test_base_agent_interface():
    # Verify all agents implement BaseAgent
    
def test_agent_registry_discovery():
    # Test agent discovery and registration
    
def test_framework_adapters_instantiate():
    # PydanticAI, CrewAI, etc. can be instantiated
```

## Known Status

### ✓ Implemented
- `.context/` directory structure (complete)
- All 00_rules files (project.md, style_guide.md, team.md)
- All 01_state files (active_session.json, task_queue.json, scratchpad.md)
- All 02_memory files (decisions.log.md, patterns.md, entities.json)
- 03_archive/sessions/ with .gitkeep

### ⏳ TODO
- Integration test scripts (test_scaffold.py, etc.)
- Actual test execution
- Pattern detection from test logs
- Learning system validation

## How This Test Suite Works

### Execution Flow
1. Test framework starts test session
2. Updates `.context/01_state/active_session.json`
3. Adds task to `.context/01_state/task_queue.json`
4. EventLogger writes test events to 03_archive/sessions/<session_id>.log.ndjson
5. Test completes and updates task status
6. PatternRecognizer analyzes log for patterns
7. Results recorded in `.context/02_memory/`

### Success Criteria
- ✓ All files properly structured
- ✓ No schema validation errors
- ✓ Event logging works correctly
- ✓ Patterns detected from logs
- ✓ No permission/permission issues

## Running Tests Manually

### Check Structure
```bash
find tests/v00/.context -type f | sort
```

**Expected**: 10 files across 4 subdirectories

### Validate JSON
```bash
python3 -m json.tool tests/v00/.context/01_state/active_session.json
python3 -m json.tool tests/v00/.context/01_state/task_queue.json
python3 -m json.tool tests/v00/.context/02_memory/entities.json
```

**Expected**: All output valid JSON with no errors

### Check Markdown
```bash
# Review content
cat tests/v00/.context/00_rules/project.md
cat tests/v00/.context/02_memory/decisions.log.md
cat tests/v00/.context/02_memory/patterns.md
```

**Expected**: Readable Markdown with proper formatting

## Debugging Tests

If tests fail, check:

1. **File Permissions**: `ls -la tests/v00/.context/`
2. **JSON Validity**: `python3 -m json.tool <file>`
3. **Directory Paths**: `find tests/v00 -type d | sort`
4. **Git Status**: `git status tests/v00/`

## Links & References

- **Framework Spec**: `FRAMEWORK.md`
- **Memory Ops Plan**: `.verdent/plans/memory-operations-system-implementation-plan-*.plan.md`
- **Agent Catalog**: `AGENTS.md`
- **Style Guide**: `tests/v00/.context/00_rules/style_guide.md`

## Next Steps

1. **Implement test_scaffold.py** - Validate directory structure
2. **Implement test_context_manager.py** - Test context loading
3. **Implement test_memory_ops.py** - Test full Memory Ops System
4. **Run full test suite** - Verify all components work
5. **Document patterns found** - Update .context/02_memory/patterns.md
6. **Archive session logs** - Move test logs to 03_archive/

---

**Created**: 2025-12-24  
**Status**: Framework Ready - Tests Pending Implementation  
**Next Action**: Implement integration test scripts
