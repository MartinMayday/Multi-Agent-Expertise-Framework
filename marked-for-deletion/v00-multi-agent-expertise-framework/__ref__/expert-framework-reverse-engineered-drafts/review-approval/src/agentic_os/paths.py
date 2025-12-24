"""
Canonical path definitions for the agentic OS structure.
"""

from pathlib import Path
from typing import Optional


class OSPaths:
    """Canonical paths for the file-based agentic OS."""
    
    def __init__(self, project_root: Path):
        self.root = Path(project_root).resolve()
    
    # Global OS directories
    @property
    def directives(self) -> Path:
        return self.root / "directives"
    
    @property
    def executions(self) -> Path:
        return self.root / "executions"
    
    @property
    def shared_kb(self) -> Path:
        return self.root / "shared-knowledgebase"
    
    @property
    def agents(self) -> Path:
        return self.root / "agents"
    
    @property
    def sessions(self) -> Path:
        return self.root / "sessions"
    
    @property
    def eval_dir(self) -> Path:
        return self.root / "eval"
    
    @property
    def test_dir(self) -> Path:
        return self.root / "test"
    
    @property
    def logs(self) -> Path:
        return self.root / "logs"
    
    @property
    def planning(self) -> Path:
        return self.root / "planning"
    
    @property
    def scripts(self) -> Path:
        return self.root / "scripts"
    
    @property
    def src(self) -> Path:
        return self.root / "src"
    
    @property
    def marked_for_deletion(self) -> Path:
        return self.root / "marked-for-deletion"
    
    @property
    def context(self) -> Path:
        return self.root / ".context"
    
    # Agent-specific paths
    def agent_dir(self, agent_name: str) -> Path:
        return self.agents / agent_name
    
    def agent_instructions(self, agent_name: str) -> Path:
        return self.agent_dir(agent_name) / f"{agent_name}_system-instructions.md"
    
    def agent_kb_manifest(self, agent_name: str) -> Path:
        return self.agent_dir(agent_name) / f"kb_{agent_name}-manifest.md"
    
    def agent_mcp_config(self, agent_name: str) -> Path:
        return self.agent_dir(agent_name) / "mcp.json"
    
    def agent_env_example(self, agent_name: str) -> Path:
        return self.agent_dir(agent_name) / ".env.example"
    
    # Canonical agent list
    CANONICAL_AGENTS = [
        "metagpt",
        "researchgpt",
        "analysisgpt",
        "designgpt",
        "implementationgpt",
        "testgpt",
        "evaluationgpt"
    ]
    
    def get_all_agent_dirs(self) -> list[Path]:
        """Get paths for all canonical agent directories."""
        return [self.agent_dir(name) for name in self.CANONICAL_AGENTS]

