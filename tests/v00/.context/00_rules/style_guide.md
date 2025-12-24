# Code Conventions and Style Guide - v00 Test Suite

## Python Code Conventions

### General Rules
- **Python Version**: 3.11+ (type hints required)
- **Style**: PEP 8 with max line length 100
- **Type Hints**: Mandatory for all functions and module-level variables
- **Docstrings**: Google-style for all public modules, classes, functions

### Testing Rules
- **Test Framework**: pytest
- **Test Files**: `test_*.py` or `*_test.py`
- **Coverage Target**: >80% for critical paths
- **Integration Tests**: Separate from unit tests in `integration/` directory
- **Mocking**: Use `unittest.mock` for external dependencies

### Imports
```python
# Standard library
import json
from pathlib import Path
from typing import Optional, Dict

# Third-party
import pytest
from pydantic import BaseModel

# Local
from src.memory import EventLogger
```

### File Operations
- Use `pathlib.Path` not `os.path`
- Check `.exists()` before reading
- Use context managers (`with` statements)
- Atomic writes for NDJSON logs

### Documentation
- Update docstrings when changing behavior
- Include examples in complex functions
- Link to `.context/00_rules/` in comments
- No commented-out code (remove or use version control)

## Commit Message Format

Follow Conventional Commits:
```
type(scope): brief description

- Detail 1
- Detail 2

Closes #123
```

Types: `feat`, `fix`, `test`, `docs`, `refactor`, `perf`

## PR Requirements
- Tests must pass
- Type checking passes (mypy if enabled)
- Docstrings updated
- CHANGELOG entry added
