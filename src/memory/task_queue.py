import json
from pathlib import Path
from typing import Any, Dict, Literal, Optional
from datetime import datetime
import uuid


class TaskQueue:
    """DOE task state management (CRUD + status transitions)."""
    
    def __init__(self, state_path: Path):
        self.state_path = Path(state_path)
        self.state_path.mkdir(parents=True, exist_ok=True)
        self.queue_file = self.state_path / "task_queue.json"
        self._ensure_queue_exists()
    
    def _ensure_queue_exists(self):
        if not self.queue_file.exists():
            self.queue_file.write_text(json.dumps({"tasks": []}, indent=2))
    
    def _load_queue(self) -> Dict[str, Any]:
        return json.loads(self.queue_file.read_text())
    
    def _save_queue(self, data: Dict[str, Any]):
        self.queue_file.write_text(json.dumps(data, indent=2))
    
    def add_task(self, content: str, priority: int = 0) -> str:
        """Add a new task to queue."""
        task_id = str(uuid.uuid4())
        queue = self._load_queue()
        
        task = {
            "id": task_id,
            "content": content,
            "status": "pending",
            "priority": priority,
            "blockers": [],
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        
        queue["tasks"].append(task)
        self._save_queue(queue)
        return task_id
    
    def update_status(self, task_id: str, status: Literal["pending", "in_progress", "completed", "blocked"]) -> bool:
        """Update task status."""
        queue = self._load_queue()
        
        for task in queue["tasks"]:
            if task["id"] == task_id:
                task["status"] = status
                task["updated_at"] = datetime.utcnow().isoformat()
                self._save_queue(queue)
                return True
        
        return False
    
    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get a single task."""
        queue = self._load_queue()
        for task in queue["tasks"]:
            if task["id"] == task_id:
                return task
        return None
    
    def get_active_task(self) -> Optional[Dict[str, Any]]:
        """Get the current in_progress task."""
        queue = self._load_queue()
        for task in queue["tasks"]:
            if task["status"] == "in_progress":
                return task
        return None
    
    def get_blocked_tasks(self) -> list[Dict[str, Any]]:
        """Get all blocked tasks."""
        queue = self._load_queue()
        return [t for t in queue["tasks"] if t["status"] == "blocked"]
    
    def add_blocker(self, task_id: str, blocker: str) -> bool:
        """Add a blocker to a task."""
        queue = self._load_queue()
        
        for task in queue["tasks"]:
            if task["id"] == task_id:
                if blocker not in task["blockers"]:
                    task["blockers"].append(blocker)
                task["updated_at"] = datetime.utcnow().isoformat()
                self._save_queue(queue)
                return True
        
        return False
    
    def get_all_tasks(self) -> list[Dict[str, Any]]:
        """Get all tasks."""
        queue = self._load_queue()
        return queue["tasks"]
