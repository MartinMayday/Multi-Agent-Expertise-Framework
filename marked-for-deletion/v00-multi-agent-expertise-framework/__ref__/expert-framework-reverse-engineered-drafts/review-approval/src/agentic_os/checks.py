"""
Validation rules for scaffold structure.
"""

from pathlib import Path
from typing import List, Tuple
from .paths import OSPaths


class ValidationResult:
    """Result of a validation check."""
    
    def __init__(self, passed: bool, message: str = "", details: List[str] = None):
        self.passed = passed
        self.message = message
        self.details = details or []
    
    def __bool__(self):
        return self.passed


class ScaffoldValidator:
    """Validates scaffold structure against FRAMEWORK requirements."""
    
    def __init__(self, paths: OSPaths):
        self.paths = paths
    
    def validate_all(self) -> List[Tuple[str, ValidationResult]]:
        """Run all validation checks."""
        results = []
        
        results.append(("directory_structure", self.validate_directory_structure()))
        results.append(("core_directives", self.validate_core_directives()))
        results.append(("agents", self.validate_agents()))
        results.append(("kb_structure", self.validate_kb_structure()))
        results.append(("root_docs", self.validate_root_docs()))
        results.append(("context_structure", self.validate_context_structure()))
        
        return results
    
    def validate_directory_structure(self) -> ValidationResult:
        """Check that all required directories exist."""
        required_dirs = [
            self.paths.directives,
            self.paths.executions,
            self.paths.shared_kb,
            self.paths.agents,
            self.paths.sessions,
            self.paths.eval_dir,
            self.paths.test_dir,
            self.paths.logs,
            self.paths.planning,
            self.paths.scripts,
            self.paths.context,
        ]
        
        missing = [d for d in required_dirs if not d.exists()]
        
        if missing:
            return ValidationResult(
                False,
                f"Missing {len(missing)} required directories",
                [str(d.relative_to(self.paths.root)) for d in missing]
            )
        
        return ValidationResult(True, "All required directories exist")
    
    def validate_core_directives(self) -> ValidationResult:
        """Check that core directives exist."""
        required = [
            "KB_GUARDRAILS.md",
            "HANDOFF_PROTOCOL.md",
            "PROGRESSIVE_LOADING.md",
            "FAILURE_HANDLING.md",
            "STAGING_AND_APPROVAL.md",
            "CONTEXT_MEMORY_SYSTEM.md",
        ]
        
        missing = []
        for name in required:
            if not (self.paths.directives / name).exists():
                missing.append(name)
        
        if missing:
            return ValidationResult(
                False,
                f"Missing {len(missing)} core directives",
                missing
            )
        
        return ValidationResult(True, "All core directives present")
    
    def validate_agents(self) -> ValidationResult:
        """Check that canonical agents are scaffolded."""
        missing = []
        incomplete = []
        
        for agent_name in OSPaths.CANONICAL_AGENTS:
            agent_dir = self.paths.agent_dir(agent_name)
            if not agent_dir.exists():
                missing.append(agent_name)
                continue
            
            # Check required files
            required_files = [
                self.paths.agent_instructions(agent_name),
                self.paths.agent_kb_manifest(agent_name),
            ]
            
            for req_file in required_files:
                if not req_file.exists():
                    incomplete.append(f"{agent_name}: {req_file.name}")
        
        if missing:
            return ValidationResult(
                False,
                f"Missing {len(missing)} agent directories",
                missing
            )
        
        if incomplete:
            return ValidationResult(
                False,
                f"{len(incomplete)} agents have incomplete structure",
                incomplete
            )
        
        return ValidationResult(True, f"All {len(OSPaths.CANONICAL_AGENTS)} agents scaffolded")
    
    def validate_kb_structure(self) -> ValidationResult:
        """Check KB manifest exists."""
        manifest = self.paths.shared_kb / "manifest.md"
        
        if not manifest.exists():
            return ValidationResult(False, "KB manifest.md missing")
        
        return ValidationResult(True, "KB structure valid")
    
    def validate_root_docs(self) -> ValidationResult:
        """Check root documentation files."""
        required = [
            "FRAMEWORK.md",
            "FRAMEWORK-CHECKLIST.md",
            "AGENTIC_WORKFLOW_CONTRACT.md",
            "AGENTS.md",
        ]
        
        missing = []
        for name in required:
            if not (self.paths.root / name).exists():
                missing.append(name)
        
        if missing:
            return ValidationResult(
                False,
                f"Missing {len(missing)} root documentation files",
                missing
            )
        
        return ValidationResult(True, "All root docs present")
    
    def validate_context_structure(self) -> ValidationResult:
        """Check that .context/ structure exists."""
        context_dir = self.paths.context
        
        if not context_dir.exists():
            return ValidationResult(False, ".context/ directory missing")
        
        # Check required core files
        core_dir = context_dir / "core"
        required_core = [
            "identity.md",
            "preferences.md",
            "workflows.md",
            "relationships.md",
            "triggers.md",
            "projects.md",
            "rules.md",
            "session.md",
            "journal.md",
        ]
        
        missing = []
        for name in required_core:
            if not (core_dir / name).exists():
                missing.append(name)
        
        # Check required root files
        required_root = ["README.md", "context-update.md"]
        for name in required_root:
            if not (context_dir / name).exists():
                missing.append(f"root/{name}")
        
        # Check conversations directory
        conversations_dir = context_dir / "conversations"
        if not conversations_dir.exists():
            missing.append("conversations/")
        
        if missing:
            return ValidationResult(
                False,
                f"Missing {len(missing)} context files/directories",
                missing
            )
        
        return ValidationResult(True, ".context/ structure valid")

