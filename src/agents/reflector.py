from pathlib import Path
from typing import Any, Dict
from datetime import datetime

from src.memory.fact_extractor import FactExtractor
from src.memory.pattern_recognizer import PatternRecognizer
from src.memory.event_logger import EventLogger


class ReflectorAgent:
    """Post-execution analysis: extracts facts, recognizes patterns, learns."""
    
    def __init__(self, memory_path: Path, archive_path: Path):
        self.memory_path = Path(memory_path)
        self.archive_path = Path(archive_path)
        
        self.fact_extractor = FactExtractor(memory_path)
        self.pattern_recognizer = PatternRecognizer(memory_path)
        self.event_logger = EventLogger(archive_path)
    
    def analyze_and_learn(self, session_id: str) -> Dict[str, Any]:
        """Analyze session, extract facts, detect patterns, generate summary."""
        
        # Load session events
        events = self.event_logger.get_session_log(session_id)
        if not events:
            return {"status": "no_events", "session_id": session_id}
        
        # Extract facts
        facts = self.fact_extractor.extract_from_log(events)
        for fact in facts:
            self.fact_extractor.save_fact(fact)
        
        # Extract entities
        full_log_text = str(events)
        entities = self.fact_extractor.extract_entities(full_log_text)
        self.fact_extractor.save_entities(entities)
        
        # Analyze patterns
        patterns = self.pattern_recognizer.analyze_session(events)
        promoted = []
        for pattern in patterns:
            if self.pattern_recognizer.should_promote(pattern):
                self.pattern_recognizer.write_pattern(pattern)
                promoted.append(pattern.name)
        
        # Generate summary
        summary = {
            "session_id": session_id,
            "analyzed_at": datetime.utcnow().isoformat(),
            "events_processed": len(events),
            "facts_extracted": len(facts),
            "entities_found": len(entities),
            "patterns_detected": len(patterns),
            "patterns_promoted": promoted,
            "status": "complete"
        }
        
        return summary
    
    def generate_session_summary(self, session_id: str) -> str:
        """Generate human-readable session summary."""
        events = self.event_logger.get_session_log(session_id)
        
        summary_lines = [
            f"# Session Summary: {session_id}",
            f"Generated: {datetime.utcnow().isoformat()}",
            "",
            f"## Statistics",
            f"- Total Events: {len(events)}",
            ""
        ]
        
        # Count event types
        event_types = {}
        for event in events:
            evt_type = event.get("type", "unknown")
            event_types[evt_type] = event_types.get(evt_type, 0) + 1
        
        summary_lines.append("## Events by Type")
        for evt_type, count in sorted(event_types.items()):
            summary_lines.append(f"- {evt_type}: {count}")
        
        summary_lines.append("")
        summary_lines.append("## Key Decisions")
        for event in events:
            if event.get("type") == "decision":
                decision = event.get("payload", {}).get("decision", "")
                if decision:
                    summary_lines.append(f"- {decision}")
        
        return "\n".join(summary_lines)
