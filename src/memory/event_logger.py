import json
from pathlib import Path
from typing import Any, Dict, Literal
from datetime import datetime
import os


class EventLogger:
    """Append-only NDJSON event logging for sessions."""
    
    def __init__(self, archive_path: Path):
        self.archive_path = Path(archive_path)
        self.archive_path.mkdir(parents=True, exist_ok=True)
        
    def _get_session_log_path(self, session_id: str) -> Path:
        return self.archive_path / f"{session_id}.log.ndjson"
    
    def log_event(self, session_id: str, event_type: str, payload: Dict[str, Any]) -> None:
        """Append a single event to session log."""
        log_path = self._get_session_log_path(session_id)
        
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "type": event_type,
            "payload": payload
        }
        
        # Atomic append with fsync
        with open(log_path, "a") as f:
            f.write(json.dumps(event) + "\n")
            os.fsync(f.fileno())
    
    def log_tool_call(self, session_id: str, tool: str, args: Dict[str, Any], result: Any) -> None:
        """Log a tool invocation."""
        self.log_event(session_id, "tool_call", {
            "tool": tool,
            "args": args,
            "result": result
        })
    
    def log_decision(self, session_id: str, decision: str, rationale: str) -> None:
        """Log an AI decision."""
        self.log_event(session_id, "decision", {
            "decision": decision,
            "rationale": rationale
        })
    
    def log_error(self, session_id: str, error_type: str, message: str, traceback_str: str = "") -> None:
        """Log an error."""
        self.log_event(session_id, "error", {
            "error_type": error_type,
            "message": message,
            "traceback": traceback_str
        })
    
    def get_session_log(self, session_id: str) -> list[Dict[str, Any]]:
        """Read all events from session log."""
        log_path = self._get_session_log_path(session_id)
        if not log_path.exists():
            return []
        
        events = []
        with open(log_path, "r") as f:
            for line in f:
                if line.strip():
                    events.append(json.loads(line))
        return events
