---
directive_id: STAGING_AND_APPROVAL
version: 1.0
enforcement_level: MANDATORY
applies_to: ALL_AGENTS
bypass_allowed: false
validation_checkpoint: PRE_WRITE
---

### WHAT THIS DIRECTIVE DOES
Prevents unauthorized writes to canonical repository locations. Forces all new/changed files through staging areas for review, validation, and approval before promotion.

### ORCHESTRATOR EXECUTION SEQUENCE

**CHECKPOINT 1: Write Location Validation**
```
BEFORE {{AGENT_NAME}} writes any file:
  
  REQUIRED_ACTION:
    - Determine write intent: {{new_file|modify_file|delete_file}}
    - Identify target canonical path: {{CANONICAL_PATH}}
  
  ENFORCEMENT:
    IF target is canonical location (not staging):
      REJECT_WRITE
      RETURN: "All writes must go to staging first. Use review-approval/ or staging/"
    
    IF target is staging area:
      ALLOW_WRITE
      LOG: "Write to staging: {{STAGING_PATH}}"
```

**CHECKPOINT 2: Changeset Creation**
```
AFTER writing to staging:
  
  REQUIRED_ACTION:
    - Create or update {{review-approval/changeset.yaml}}
    - Document: {{what_changed}}, {{why_changed}}, {{target_canonical_path}}
  
  REQUIRED_OUTPUT:
    - changeset_id: {{UNIQUE_ID}}
    - files: [{{source: staging_path, target: canonical_path}}]
    - description: {{WHY_THIS_CHANGE}}
  
  ENFORCEMENT:
    IF changeset missing:
      MARK_INCOMPLETE
      RETURN: "Changeset required for all staged changes"
```

**CHECKPOINT 3: Validation Gate**
```
BEFORE promotion request:
  
  REQUIRED_ACTION:
    - Run {{python scripts/validate_scaffold.py --project-root . -v}}
    - Run relevant tests (if applicable)
    - Check for secrets/sensitive data
  
  REQUIRED_OUTPUT:
    - validation_status: {{pass|fail|partial}}
    - test_results: {{pass|fail|n/a}}
    - security_check: {{pass|fail}}
  
  ENFORCEMENT:
    IF validation fails:
      BLOCK_PROMOTION
      RETURN: "Validation must pass before promotion"
```

**CHECKPOINT 4: Approval Checklist**
```
BEFORE promotion:
  
  REQUIRED_ACTION:
    - Generate promotion checklist:
      • Scaffold validation passes
      • All tests pass (if applicable)
      • No secrets or sensitive data
      • Files follow filesystem-as-API contract
      • KB snippets have proper source attribution
      • Documentation updated if needed
  
  REQUIRED_OUTPUT:
    - approval_checklist: {{COMPLETED_CHECKLIST}}
    - approval_status: {{pending|approved|rejected}}
  
  ENFORCEMENT:
    IF approval_status != "approved":
      BLOCK_PROMOTION
      RETURN: "Human approval required"
```

**CHECKPOINT 5: Promotion Execution**
```
ONLY AFTER validation + approval:
  
  REQUIRED_ACTION:
    - Use {{/promote-staged-changes}} command or promotion script
    - Move files from {{STAGING_PATH}} to {{CANONICAL_PATH}}
    - Update changeset: {{approval_status: approved, promoted_at: TIMESTAMP}}
  
  REQUIRED_OUTPUT:
    - Promotion log: {{FILES_PROMOTED}}
    - Post-promotion validation: {{pass|fail}}
  
  ENFORCEMENT:
    IF post-promotion validation fails:
      ROLLBACK if possible
      LOG: "Promotion validation failure"
```

### ALLOWED WRITE PATHS (Default)

**Staging Areas (Always Allowed):**
- `review-approval/` - For human-reviewed changes
- `staging/` - For machine outputs and temporary files
- `sessions/` - For agent execution history (agent-specific)
- `logs/` - For execution logs
- `.context/` - For repo-context memory (runtime-writable with strict rules):
  - Transcripts: append-only, never modify after creation
  - No secrets: redact all sensitive data
  - Follow structure: use core/ files and conversations/ directory
  - Prefer summaries/links when possible, but full transcripts allowed

**Canonical Locations (Require Promotion):**
- `directives/` - Only after staging approval
- `executions/` - Only after staging approval
- `shared-knowledgebase/` - Only after staging approval
- `agents/` - Only after staging approval
- Root documentation files - Only after staging approval

### FORBIDDEN ACTIONS

- ❌ Direct writes to canonical locations without staging
- ❌ Promotion without validation
- ❌ Promotion without approval
- ❌ Skipping changeset creation
- ❌ Writing secrets or sensitive data (even to staging)

### EXCEPTIONS

**Explicit User Permission:**
- IF user explicitly requests direct write to canonical location:
  - Log: "Direct write authorized by user"
  - Still create changeset for audit trail
  - Skip staging but still require validation

**Read-Only Operations:**
- Reading files from canonical locations is always allowed
- Reading from staging is always allowed

### VALIDATION CRITERIA

Directive is SUCCESSFUL when:
- ✓ No files written directly to canonical locations (except with explicit permission)
- ✓ All staged changes have changeset.yaml entries
- ✓ All promotions pass validation
- ✓ All promotions have approval
- ✓ Audit trail complete (changeset + promotion log)

