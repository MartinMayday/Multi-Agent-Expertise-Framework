# Style Guide

## Code Conventions

### Python
- Python 3.11+
- Type hints required (mypy strict mode)
- PEP 8 compliant
- Use pathlib.Path for file operations
- Use pydantic for data validation

### File Organization
- `src/` for application code
- `tests/` for test suites
- `0_directives/` for policies and workflows
- `1_orchestration/` for agent definitions and mental models
- `2_executions/` for tools and utilities
- `3_state/` for operational memory

## Documentation
- README.md at project root
- FRAMEWORK.md explaining architecture
- Docstrings in reStructuredText format
- Comments explain "why", not "what"

## Commit Message Format
Follow Conventional Commits:
```
type(scope): description

- detail 1
- detail 2
```

Types: feat, fix, docs, refactor, test, chore

## PR Requirements
- All tests passing
- Type checking (mypy) passing
- Lint (flake8/ruff) passing
- Documentation updated
