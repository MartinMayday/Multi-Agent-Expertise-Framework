# Executions

This directory contains pre-built Python tools and workflows that agents execute.

## Structure

- `tools/` - Single-purpose utilities
- `workflows/` - Multi-step processes
- `utils/` - Shared utilities (providers, context_manager, error_handler, logging_config)
- `eval/` - Evaluation scripts for tool outputs
- `hooks/` - Agent lifecycle hooks (pre_execution, post_execution, on_error)

## Usage

Agents reference tools from this directory via their system instructions. Tools are deterministic Python scripts that:
- Accept inputs from directives
- Execute computation/logic
- Return structured outputs
- Update context/KB as needed

## Adding New Tools

1. Create tool in `tools/` or `workflows/`
2. Add to agent's system-instructions.md tool list
3. Document in this README
4. Add tests in `test/`

