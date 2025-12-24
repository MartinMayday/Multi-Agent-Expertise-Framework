import json
from pathlib import Path
from typing import Any, Dict, List, Tuple
from datetime import datetime
import re


class Fact:
    """Triplet: (Subject, Predicate, Object) with confidence."""
    
    def __init__(self, subject: str, predicate: str, obj: str, confidence: float = 0.8, source: str = ""):
        self.subject = subject
        self.predicate = predicate
        self.object = obj
        self.confidence = confidence
        self.source = source
        self.created_at = datetime.utcnow().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "subject": self.subject,
            "predicate": self.predicate,
            "object": self.object,
            "confidence": self.confidence,
            "source": self.source,
            "created_at": self.created_at
        }


class Entity:
    """Named entity: name, type, value, description."""
    
    def __init__(self, name: str, entity_type: str, value: str, description: str = ""):
        self.name = name
        self.type = entity_type
        self.value = value
        self.description = description
        self.last_verified = datetime.utcnow().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "type": self.type,
            "value": self.value,
            "description": self.description,
            "last_verified": self.last_verified
        }


class FactExtractor:
    """Extract triplets and entities from session logs."""
    
    def __init__(self, memory_path: Path):
        self.memory_path = Path(memory_path)
        self.memory_path.mkdir(parents=True, exist_ok=True)
        self.facts_file = self.memory_path / "facts.ndjson"
        self.entities_file = self.memory_path / "entities.json"
    
    def extract_from_log(self, events: List[Dict[str, Any]]) -> List[Fact]:
        """Parse session log events for extractable facts."""
        facts = []
        
        for event in events:
            if event.get("type") == "decision":
                payload = event.get("payload", {})
                decision = payload.get("decision", "")
                
                # Simple pattern: extract "X is Y" patterns
                match = re.search(r"(\w+)\s+(?:is|are)\s+(.+?)(?:\.|$)", decision)
                if match:
                    subject, obj = match.groups()
                    fact = Fact(
                        subject=subject.strip(),
                        predicate="is",
                        obj=obj.strip(),
                        confidence=0.7,
                        source=f"event:{event.get('type')}"
                    )
                    facts.append(fact)
            
            elif event.get("type") == "tool_call":
                payload = event.get("payload", {})
                tool = payload.get("tool", "")
                
                # Extract: Tool X was called with args Y
                if tool:
                    fact = Fact(
                        subject=tool,
                        predicate="used_with",
                        obj=json.dumps(payload.get("args", {})),
                        confidence=0.9,
                        source=f"event:tool_call"
                    )
                    facts.append(fact)
        
        return facts
    
    def extract_entities(self, text: str) -> List[Entity]:
        """Extract named entities from text."""
        entities = []
        
        # Pattern: URLs
        urls = re.findall(r"https?://\S+", text)
        for url in urls:
            entities.append(Entity(
                name=url,
                entity_type="url",
                value=url
            ))
        
        # Pattern: File paths
        paths = re.findall(r"(/[\w/\-\.]+)", text)
        for path in paths:
            entities.append(Entity(
                name=path,
                entity_type="path",
                value=path
            ))
        
        # Pattern: Function/Class names (PascalCase or snake_case followed by parentheses)
        identifiers = re.findall(r"([A-Z][a-zA-Z]*|[a-z_]+)\(\)", text)
        for identifier in identifiers:
            entities.append(Entity(
                name=identifier,
                entity_type="function",
                value=identifier
            ))
        
        return entities
    
    def save_fact(self, fact: Fact) -> None:
        """Append fact to facts log (append-only)."""
        with open(self.facts_file, "a") as f:
            f.write(json.dumps(fact.to_dict()) + "\n")
    
    def save_entities(self, entities: List[Entity]) -> None:
        """Save entities to JSON."""
        all_entities = {}
        
        if self.entities_file.exists():
            all_entities = json.loads(self.entities_file.read_text())
        
        for entity in entities:
            key = f"{entity.type}:{entity.name}"
            all_entities[key] = entity.to_dict()
        
        self.entities_file.write_text(json.dumps(all_entities, indent=2))
    
    def get_facts(self) -> List[Dict[str, Any]]:
        """Read all facts from log."""
        if not self.facts_file.exists():
            return []
        
        facts = []
        with open(self.facts_file, "r") as f:
            for line in f:
                if line.strip():
                    facts.append(json.loads(line))
        
        return facts
    
    def get_entities(self) -> Dict[str, Any]:
        """Read all entities."""
        if not self.entities_file.exists():
            return {}
        
        return json.loads(self.entities_file.read_text())
