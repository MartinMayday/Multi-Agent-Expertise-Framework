# Memory Operations System - Instructions

## Core Principle
You are responsible for maintaining the system's persistent memory. Every significant decision, learning, and state change must be recorded.

## Memory Layers
1. **Rules (00_rules/)**: Immutable project constitution and coding standards.
2. **State (01_state/)**: Active session data, task queues, and scratchpads.
3. **Memory (02_memory/)**: Learned patterns, extracted facts, and entities.
4. **Archive (03_archive/)**: Historical session logs and conversation transcripts.

## Update Protocol
- **Autonomous Updates**: Update memory files as you learn. No need to ask for permission for routine updates.
- **Decision Logging**: Record every architectural or strategy decision in `02_memory/decisions.log.md`.
- **Fact Extraction**: Periodically extract facts from sessions into `02_memory/learned_facts.ndjson`.
