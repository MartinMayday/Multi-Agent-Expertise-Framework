# Missing Files Checklist

**Generated**: 2024-12-23  
**Purpose**: Checklist of all files that need to be generated to complete the Expert Framework Agentic OS

## Phase 3: Agent System Instructions

### MetaGPT (`agents/metagpt/`)
- [ ] Update `metagpt_system-instructions.md` with:
  - [ ] KB-first guardrails from `directives/KB_GUARDRAILS.md`
  - [ ] Handoff protocol from `directives/HANDOFF_PROTOCOL.md`
  - [ ] Progressive loading from `directives/PROGRESSIVE_LOADING.md`
  - [ ] Staging policy from `directives/STAGING_AND_APPROVAL.md`
  - [ ] Model selection via .env
  - [ ] MCP tool configuration
- [ ] Populate `kb_metagpt-manifest.md` with initial knowledge
- [ ] Create test cases in `test/`
- [ ] Create eval metrics in `eval/`

### ResearchGPT (`agents/researchgpt/`)
- [ ] Update `researchgpt_system-instructions.md` with:
  - [ ] KB-first guardrails
  - [ ] Web search/scrape tool configuration
  - [ ] Source attribution requirements
  - [ ] KB snippet generation workflow
- [ ] Populate `kb_researchgpt-manifest.md`
- [ ] Create test cases in `test/`
- [ ] Create eval metrics in `eval/`

### AnalysisGPT (`agents/analysisgpt/`)
- [ ] Update `analysisgpt_system-instructions.md` with:
  - [ ] KB-first guardrails
  - [ ] Pattern extraction methodology
  - [ ] Synthesis rules
- [ ] Populate `kb_analysisgpt-manifest.md`
- [ ] Create test cases in `test/`
- [ ] Create eval metrics in `eval/`

### DesignGPT (`agents/designgpt/`)
- [ ] Update `designgpt_system-instructions.md` with:
  - [ ] KB-first guardrails
  - [ ] System design principles
  - [ ] Architecture patterns
- [ ] Populate `kb_designgpt-manifest.md`
- [ ] Create test cases in `test/`
- [ ] Create eval metrics in `eval/`

### ImplementationGPT (`agents/implementationgpt/`)
- [ ] Update `implementationgpt_system-instructions.md` with:
  - [ ] KB-first guardrails
  - [ ] Spec adherence rules
  - [ ] Missing input detection
- [ ] Populate `kb_implementationgpt-manifest.md`
- [ ] Create test cases in `test/`
- [ ] Create eval metrics in `eval/`

### TestGPT (`agents/testgpt/`)
- [ ] Update `testgpt_system-instructions.md` with:
  - [ ] KB-first guardrails
  - [ ] Validation protocols
  - [ ] Failure mode analysis
- [ ] Populate `kb_testgpt-manifest.md`
- [ ] Create test cases in `test/`
- [ ] Create eval metrics in `eval/`

### EvaluationGPT (`agents/evaluationgpt/`)
- [ ] Update `evaluationgpt_system-instructions.md` with:
  - [ ] KB-first guardrails
  - [ ] Go/no-go decision criteria
  - [ ] Handoff coordination rules
- [ ] Populate `kb_evaluationgpt-manifest.md`
- [ ] Create test cases in `test/`
- [ ] Create eval metrics in `eval/`

---

## Phase 4: Execution Tools

### Core Utilities (`executions/tools/`)
- [ ] `kb_snippet_validator.py` - Validate KB snippet format
- [ ] `changeset_validator.py` - Validate changeset.yaml
- [ ] `promotion_script.py` - Promote staged changes after approval
- [ ] `handoff_validator.py` - Validate handoff contracts
- [ ] README.md for each tool

### Workflow Tools (`executions/workflows/`)
- [ ] `plan_executor.py` - Execute planning workflow
- [ ] `build_executor.py` - Execute build workflow
- [ ] `self_improve_executor.py` - Execute self-improvement workflow
- [ ] `plan_build_improve.py` - Chained workflow executor
- [ ] README.md for each workflow

### Evaluation Tools (`executions/eval/`)
- [ ] `maturity_scorer.py` - Calculate agent maturity scores
- [ ] `reliability_tracker.py` - Track agent reliability metrics
- [ ] `kb_coverage_analyzer.py` - Analyze KB completeness
- [ ] `handoff_success_tracker.py` - Track handoff success rates
- [ ] README.md for each tool

### Utils (`executions/utils/`)
- [ ] `path_helpers.py` - Path manipulation utilities
- [ ] `yaml_helpers.py` - YAML parsing/validation
- [ ] `validation_helpers.py` - Common validation functions
- [ ] README.md for utils

### Hooks (`executions/hooks/`)
- [ ] `pre_execution_hook.py` - Pre-execution validation
- [ ] `post_execution_hook.py` - Post-execution cleanup
- [ ] `evaluation_hook.py` - Trigger evaluation after execution
- [ ] README.md for hooks

### Executions README
- [ ] `executions/README.md` - Documentation for all execution tools

---

## Phase 5: Knowledge Base

### Framework Knowledge (`shared-knowledgebase/snippets/`)
- [ ] `expert-framework-patterns.md` - Expert framework patterns
- [ ] `filesystem-as-api-contract.md` - Filesystem-as-API documentation
- [ ] `agent-orchestration-patterns.md` - Agent orchestration patterns
- [ ] `context-engineering-principles.md` - Context engineering principles
- [ ] `kb-first-execution.md` - KB-first execution methodology
- [ ] `progressive-loading.md` - Progressive loading patterns
- [ ] `handoff-protocol.md` - Handoff protocol examples
- [ ] `staging-approval-workflow.md` - Staging and approval workflow

### Domain Knowledge (`shared-knowledgebase/snippets/`)
- [ ] Domain-specific expertise snippets (as needed)
- [ ] Tool usage patterns
- [ ] Workflow examples
- [ ] Failure recovery patterns

### KB Maintenance
- [ ] `shared-knowledgebase/manifest.md` - Update with all snippets
- [ ] KB snippet review process documentation
- [ ] KB update workflow documentation
- [ ] KB deduplication tool (if needed)

---

## Phase 6: Testing

### Unit Tests (`test/`)
- [ ] `test_execution_tools.py` - Test execution tools
- [ ] `test_validation_scripts.py` - Test validation scripts
- [ ] `test_kb_operations.py` - Test KB operations
- [ ] `test_handoff_contracts.py` - Test handoff contracts
- [ ] `test_staging_promotion.py` - Test staging/promotion flow

### Integration Tests (`test/`)
- [ ] `test_agent_workflows.py` - Test agent workflows
- [ ] `test_staging_flow.py` - Test staging/promotion flow
- [ ] `test_kb_first_execution.py` - Test KB-first execution
- [ ] `test_handoff_protocol.py` - Test handoff protocol

### End-to-End Tests (`test/`)
- [ ] `test_plan_build_improve_cycle.py` - Test complete cycle
- [ ] `test_multi_agent_orchestration.py` - Test multi-agent workflows
- [ ] `test_failure_recovery.py` - Test failure recovery
- [ ] `test_knowledge_accumulation.py` - Test knowledge accumulation

### Test Framework
- [ ] `test/README.md` - Test framework documentation
- [ ] `test/conftest.py` - Pytest configuration
- [ ] `test/fixtures/` - Test fixtures

---

## Phase 7: Evaluation

### Metrics Definition (`eval/`)
- [ ] `metrics_definition.md` - Define all metrics
- [ ] `agent_reliability_metrics.md` - Agent reliability definitions
- [ ] `kb_completeness_metrics.md` - KB completeness definitions
- [ ] `response_quality_metrics.md` - Response quality definitions
- [ ] `tool_correctness_metrics.md` - Tool correctness definitions

### Evaluation Implementation (`executions/eval/`)
- [ ] `maturity_scorer.py` - Implement maturity scoring
- [ ] `reliability_tracker.py` - Implement reliability tracking
- [ ] `quality_analyzer.py` - Implement quality analysis
- [ ] `evaluation_dashboard.py` - Create evaluation dashboard

### Evaluation Documentation
- [ ] `eval/README.md` - Evaluation framework documentation
- [ ] `eval/schedule.md` - Evaluation schedule
- [ ] `eval/improvement_loop.md` - Improvement feedback loop

---

## Phase 8: Documentation

### User Documentation
- [ ] `docs/getting-started.md` - Getting started guide
- [ ] `docs/agent-usage.md` - Agent usage guide
- [ ] `docs/tool-development.md` - Tool development guide
- [ ] `docs/kb-contribution.md` - KB contribution guide

### Developer Documentation
- [ ] `docs/architecture-decisions.md` - Architecture decisions
- [ ] `docs/extension-points.md` - Extension points
- [ ] `docs/testing-strategy.md` - Testing strategy
- [ ] `docs/deployment-process.md` - Deployment process

### Handoff Materials
- [ ] `docs/project-summary.md` - Project summary
- [ ] `docs/known-issues.md` - Known issues list
- [ ] `docs/future-roadmap.md` - Future roadmap
- [ ] `docs/maintenance-guide.md` - Maintenance guide

### Documentation Structure
- [ ] `docs/README.md` - Documentation index
- [ ] `docs/` directory structure

---

## Configuration Files

### Agent Configuration
- [ ] `.env.example` files for each agent (already scaffolded, need to populate)
- [ ] `mcp.json` files for each agent (already scaffolded, need to configure)

### Global Configuration
- [ ] `.env.example` at root (if needed)
- [ ] `mcp.json` at root (if needed)

---

## Summary

**Total Missing Files**: ~100+ files across 8 phases

**Priority Order**:
1. Phase 3: Agent System Instructions (7 agents × ~4 files = 28 files)
2. Phase 4: Execution Tools (~15 files)
3. Phase 5: Knowledge Base (~10 files)
4. Phase 6: Testing (~15 files)
5. Phase 7: Evaluation (~8 files)
6. Phase 8: Documentation (~12 files)

**Next Session**: Start with Phase 3, Task 3.1 (MetaGPT System Instructions)

---

## Notes

- All files must be staged in `review-approval/` before promotion
- Use `/stage-changes` command to create changeset
- Use `/promote-staged-changes` only after validation + approval
- Update `planning/WORKSESSION_STATE.md` after each file completion
- Update `planning/ROADMAP.md` as phases complete

