---
allowed-tools: Bash(git ls-files:*), Read, Write
description: Answer questions about the project structure and documentation with Mermaid diagrams
argument-hint: [question]
model: opus
---

# Purpose

Answer the user's question by analyzing the project structure and documentation, then enhance the response with relevant Mermaid diagrams that visualize key concepts, relationships, or flow. This prompt provides comprehensive answers with visual aids while following the `Instructions` section guidelines.


## Variables

USER_QUESTION: $1

## Instructions

- **IMPORTANT: This is primarily q question-answering task - focus on providing information answers**
- **IMPORTANT: Ehance answers with Mermaid diagrams to visuals concepts, relationships, and flows**
- **IMPORTANT: Use appropriate diagrams types based on the question context**
    - `flowchart` - for processes, workflows, and decisions trees
    - `sequenceDiagram` - for interactions between components/systems
    - `classDiagram` - for class relationships and structures
    - `erDiagram` - for database/entity relationships
    - `graph` - for general relationships and hierarchies
    - `stateDiagram-v2` - for state machines and transitions
    - `mindmap` - for concept organization and brainstorming
- **IMPORTANT: Diagrams should clarify and enhance understanding, not replace textual explanations**
- **IMPORTANT: If the questions requires code changes, explain conceptually with diagrams showing proposed architecture**


## Workflow

1. Run `git ls-files` to understand the project structure
2. Read README.md for project overview and documentation
3. Analyze the project structure to identify relevant files and components
4. Read additional files as neededto answer the question thoroughly
5. Formulate a comprehensive textual answer
6. Determine which diagrams type(s) best visualize the answer
7. Create Mermaid diagrams(s) that enhance understanding
8. Combine textual answer with diagrams in the response


## Report