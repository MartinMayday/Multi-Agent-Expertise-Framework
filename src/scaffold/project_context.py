from pathlib import Path
import json


class ProjectContextScaffold:
    """Create `.context/` structure in a project."""
    
    def __init__(self, project_root: Path):
        self.project_root = Path(project_root)
        self.context_root = self.project_root / ".context"
    
    def create_scaffold(self) -> bool:
        """Create complete .context/ structure."""
        try:
            # Create main directories
            (self.context_root / "00_rules").mkdir(parents=True, exist_ok=True)
            (self.context_root / "01_state").mkdir(parents=True, exist_ok=True)
            (self.context_root / "02_memory").mkdir(parents=True, exist_ok=True)
            (self.context_root / "03_archive" / "sessions").mkdir(parents=True, exist_ok=True)
            
            # Create 00_rules files
            self._create_project_md()
            self._create_style_guide()
            self._create_team_md()
            
            # Create 01_state files
            self._create_active_session()
            self._create_task_queue()
            self._create_scratchpad()
            
            # Create 02_memory files
            self._create_decisions_log()
            self._create_patterns_md()
            self._create_entities_json()
            
            # Create context-update.md at root
            self._create_context_update()
            
            return True
        except Exception as e:
            print(f"Error creating scaffold: {e}")
            return False
    
    def _create_project_md(self):
        path = self.context_root / "00_rules" / "project.md"
        if not path.exists():
            path.write_text("""# Project Constitution

## Mission
Define your project's mission, core values, and strategic goals.

## Architecture
Describe the system architecture and key design decisions.

## Success Metrics
Define what success looks like for this project.
""")
    
    def _create_style_guide(self):
        path = self.context_root / "00_rules" / "style_guide.md"
        if not path.exists():
            path.write_text("""# Style Guide

## Code Conventions
- Language: 
- Framework:
- Key patterns:

## Documentation
- Comment style:
- README format:
- Examples:

## Commit Message Format
Follows Conventional Commits: `type: description`
""")
    
    def _create_team_md(self):
        path = self.context_root / "00_rules" / "team.md"
        if not path.exists():
            path.write_text("""# Team & Roles

## Team Members
- Name: Role, responsibilities

## Communication Protocol
- Async: Decision logs, PRs
- Sync: Code review, planning

## Decision Making
How are architectural decisions made and documented?
""")
    
    def _create_active_session(self):
        path = self.context_root / "01_state" / "active_session.json"
        if not path.exists():
            data = {
                "id": None,
                "goal": None,
                "start_time": None,
                "status": "inactive",
                "agent": None,
                "step": 0
            }
            path.write_text(json.dumps(data, indent=2))
    
    def _create_task_queue(self):
        path = self.context_root / "01_state" / "task_queue.json"
        if not path.exists():
            data = {"tasks": []}
            path.write_text(json.dumps(data, indent=2))
    
    def _create_scratchpad(self):
        path = self.context_root / "01_state" / "scratchpad.md"
        if not path.exists():
            path.write_text("""# Scratchpad

Shared whiteboard for agent collaboration during current session.

## Current Focus
(What are we working on right now?)

## Blockers
(What's preventing progress?)

## Next Steps
(What comes next?)
""")
    
    def _create_decisions_log(self):
        path = self.context_root / "02_memory" / "decisions.log.md"
        if not path.exists():
            path.write_text("""# Decision Log

Architectural Decision Records (ADRs) for this project.

## Format
Each decision should include:
- Decision date
- What was decided
- Why (context and alternatives)
- Consequences

---

""")
    
    def _create_patterns_md(self):
        path = self.context_root / "02_memory" / "patterns.md"
        if not path.exists():
            path.write_text("""# Learned Patterns

Project-specific patterns discovered through experience.

## Format
- Pattern name
- When it applies
- How to use it
- Examples

---

""")
    
    def _create_entities_json(self):
        path = self.context_root / "02_memory" / "entities.json"
        if not path.exists():
            data = {}
            path.write_text(json.dumps(data, indent=2))
    
    def _create_context_update(self):
        path = self.context_root / "context-update.md"
        if not path.exists():
            path.write_text("""# How to Update Context

This file explains how to maintain the `.context/` system.

## Workflow

1. **Session starts**: Agent loads `00_rules/` and `01_state/`
2. **During execution**: Agent updates `01_state/scratchpad.md` and logs events
3. **Session ends**: EventLogger writes to `03_archive/sessions/`
4. **Post-execution**: ReflectorAgent extracts facts and patterns to `02_memory/`

## Files to Edit

### 00_rules/ (Immutable)
- Only edit when project changes fundamentally
- Commit these changes

### 01_state/ (Ephemeral)
- Updated during sessions
- Can be archived/reset

### 02_memory/ (Append-only)
- Self-annealing facts and patterns
- Should not be deleted

### 03_archive/ (Historical)
- Session logs stored here
- Searchable for debugging
""")
