import json
from pathlib import Path
from typing import Dict, Any

class ContextManager:
    """Consolidated path resolution for Global (~/.expert-framework) and Project (.context) memory."""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.global_root = Path.home() / ".expert-framework"
        
    def resolve_project(self, layer: str) -> Path:
        return self.project_root / "3_state" / layer

    def resolve_global(self, file: str) -> Path:
        return self.global_root / file

    def load_merged_rules(self) -> str:
        """Merge global guardrails with project constitution."""
        global_rules = self.resolve_global("global_rules.md")
        project_rules = self.resolve_project("00_rules")
        
        content = []
        if global_rules.exists():
            content.append(global_rules.read_text())
        
        for f in project_rules.glob("*.md"):
            content.append(f.read_text())
            
        return "\n\n".join(content)
