# Agent Catalog

This catalog lists all available agents in the system. Agents can reference this to discover capabilities and request delegation.

## MetaGPT (Orchestrator)
- **Role**: Prompt decomposition and workflow coordination
- **Invocation**: Automatic on braindump prompts
- **Model**: claude-sonnet-4.5
- **Tools**: None (orchestration only)
- **Location**: agents/metagpt/

## ResearchGPT
- **Role**: Documentation-first research
- **Triggers**: "research", "find documentation", "gather info"
- **Model**: claude-sonnet-4.5
- **Tools**: web.search, web.scrape, web.fetch
- **Location**: agents/researchgpt/

## AnalysisGPT
- **Role**: Pattern extraction and synthesis
- **Triggers**: "analyze", "synthesize", "compare"
- **Model**: claude-sonnet-4.5
- **Tools**: None (analysis only)
- **Location**: agents/analysisgpt/

## DesignGPT
- **Role**: System design and architecture
- **Triggers**: "design", "architect", "plan system"
- **Model**: claude-sonnet-4.5
- **Tools**: None (design only)
- **Location**: agents/designgpt/

## ImplementationGPT
- **Role**: Code generation from specifications
- **Triggers**: "implement", "build", "code"
- **Model**: claude-sonnet-4.5
- **Tools**: Write, Read, Bash
- **Location**: agents/implementationgpt/

## TestGPT
- **Role**: Validation and testing
- **Triggers**: "test", "validate", "verify"
- **Model**: claude-sonnet-4.5
- **Tools**: Bash, Read
- **Location**: agents/testgpt/

## EvaluationGPT
- **Role**: Go/no-go decisions and handoff coordination
- **Triggers**: "evaluate", "decide", "handoff"
- **Model**: claude-sonnet-4.5
- **Tools**: Read, Write (reports only)
- **Location**: agents/evaluationgpt/

## Request New Agent
If no existing agent fits your needs, return to MetaGPT with:
- Required capabilities
- Expected inputs/outputs
- Suggested name
