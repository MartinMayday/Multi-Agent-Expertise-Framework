import json
from pathlib import Path
from typing import Any, Dict, List
from datetime import datetime
from collections import Counter


class Pattern:
    """Learned pattern: repeated behavior, error, or success."""
    
    def __init__(self, name: str, description: str, occurrences: int = 1, 
                 confidence: float = 0.5, category: str = "heuristic"):
        self.name = name
        self.description = description
        self.occurrences = occurrences
        self.confidence = confidence
        self.category = category  # heuristic, error_pattern, success_pattern
        self.discovered_at = datetime.utcnow().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "occurrences": self.occurrences,
            "confidence": self.confidence,
            "category": self.category,
            "discovered_at": self.discovered_at
        }


class PatternRecognizer:
    """Detect repeated failures/successes and generate heuristic rules."""
    
    def __init__(self, memory_path: Path):
        self.memory_path = Path(memory_path)
        self.memory_path.mkdir(parents=True, exist_ok=True)
        self.patterns_file = self.memory_path / "patterns.md"
        self._ensure_patterns_file()
    
    def _ensure_patterns_file(self):
        if not self.patterns_file.exists():
            self.patterns_file.write_text("# Learned Patterns\n\n")
    
    def analyze_session(self, events: List[Dict[str, Any]]) -> List[Pattern]:
        """Detect patterns in session log."""
        patterns = []
        
        # Count error types
        error_types = [e for e in events if e.get("type") == "error"]
        error_counter = Counter(e.get("payload", {}).get("error_type") for e in error_types)
        
        for error_type, count in error_counter.items():
            if count >= 2 and error_type:  # 2+ occurrences
                pattern = Pattern(
                    name=f"repeated_{error_type}",
                    description=f"Error '{error_type}' occurred {count} times in session",
                    occurrences=count,
                    confidence=min(count / 10, 0.9),
                    category="error_pattern"
                )
                patterns.append(pattern)
        
        # Count tool usage
        tool_calls = [e for e in events if e.get("type") == "tool_call"]
        tool_counter = Counter(e.get("payload", {}).get("tool") for e in tool_calls)
        
        for tool, count in tool_counter.items():
            if count >= 2 and tool:
                pattern = Pattern(
                    name=f"frequent_{tool}_usage",
                    description=f"Tool '{tool}' was called {count} times",
                    occurrences=count,
                    confidence=0.7,
                    category="heuristic"
                )
                patterns.append(pattern)
        
        return patterns
    
    def should_promote(self, pattern: Pattern) -> bool:
        """Determine if pattern is significant enough to promote to rules."""
        # Promote if 2+ occurrences
        return pattern.occurrences >= 2
    
    def write_pattern(self, pattern: Pattern, scope: str = "project") -> None:
        """Add pattern to patterns.md."""
        content = self.patterns_file.read_text()
        
        pattern_md = f"""## {pattern.name}

**Category**: {pattern.category}  
**Occurrences**: {pattern.occurrences}  
**Confidence**: {pattern.confidence:.1%}  
**Discovered**: {pattern.discovered_at}  
**Scope**: {scope}  

{pattern.description}

---

"""
        
        self.patterns_file.write_text(content + pattern_md)
    
    def get_patterns(self) -> str:
        """Read all patterns from file."""
        if self.patterns_file.exists():
            return self.patterns_file.read_text()
        return ""
    
    def get_high_confidence_patterns(self, threshold: float = 0.7) -> List[Dict[str, Any]]:
        """Get patterns above confidence threshold."""
        patterns = []
        content = self.get_patterns()
        
        # Parse markdown patterns (simplified)
        # In production, would use structured format
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if line.startswith("**Confidence**"):
                conf_str = line.split(": ")[1].rstrip("%")
                try:
                    conf = float(conf_str) / 100
                    if conf >= threshold:
                        patterns.append({"confidence": conf, "line": i})
                except ValueError:
                    pass
        
        return patterns
