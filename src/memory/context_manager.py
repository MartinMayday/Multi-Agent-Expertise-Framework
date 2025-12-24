import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

class ContextManager:
    def __init__(self, project_root: Optional[str] = None):
        self.project_root = Path(project_root or os.getcwd())
        self.global_root = Path.home() / ".expert-framework"
        
    def get_project_path(self, relative_path: str) -> Path:
        return self.project_root / "3_state" / relative_path

    def get_global_path(self, relative_path: str) -> Path:
        return self.global_root / relative_path

    def load_json(self, path: Path) -> Dict[str, Any]:
        if not path.exists():
            return {}
        with open(path, 'r') as f:
            return json.load(f)

    def save_json(self, path: Path, data: Dict[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)

    def load_rules(self) -> str:
        project_rules = self.get_project_path("00_rules")
        global_rules = self.get_global_path("global_rules.md")
        
        rules = []
        if global_rules.exists():
            rules.append(global_rules.read_text())
        
        if project_rules.exists():
            for rule_file in project_rules.glob("*.md"):
                rules.append(rule_file.read_text())
                
        return "\n\n".join(rules)
