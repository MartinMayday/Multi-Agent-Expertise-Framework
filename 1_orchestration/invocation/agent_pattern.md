# Agent Invocation Pattern

## Format
`@agent-<name> [prompt]`

## Examples
- `@agent-planner create a plan for feature X`
- `@agent-meta-agent create a database expert agent`
- `@agent-database-expert How does our schema work?`
- `@agent-researchgpt find documentation for PydanticAI`

## Standard Agents
- `metagpt`: Orchestrator agent.
- `researchgpt`: Documentation-first research.
- `analysisgpt`: Pattern extraction and synthesis.
- `designgpt`: System design and architecture.
- `implementationgpt`: Code generation.
- `testgpt`: Validation and testing.
- `evaluationgpt`: Go/no-go decisions.
