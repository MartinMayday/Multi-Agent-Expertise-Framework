#!/usr/bin/env python3
"""
Validate scaffold structure against FRAMEWORK requirements.

Usage:
    python scripts/validate_scaffold.py [--project-root PATH]
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agentic_os.paths import OSPaths
from agentic_os.checks import ScaffoldValidator


def main():
    parser = argparse.ArgumentParser(
        description="Validate scaffold structure"
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path.cwd(),
        help="Project root directory (default: current directory)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed validation results"
    )
    
    args = parser.parse_args()
    
    paths = OSPaths(args.project_root)
    validator = ScaffoldValidator(paths)
    
    print(f"Validating scaffold in: {paths.root}\n")
    
    results = validator.validate_all()
    
    passed = 0
    failed = 0
    
    for check_name, result in results:
        status = "✓" if result.passed else "✗"
        print(f"{status} {check_name}: {result.message}")
        
        if result.passed:
            passed += 1
        else:
            failed += 1
            if args.verbose and result.details:
                for detail in result.details:
                    print(f"    - {detail}")
    
    print(f"\n{'='*50}")
    print(f"Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("✓ Scaffold validation PASSED")
        return 0
    else:
        print("✗ Scaffold validation FAILED")
        print("\nFix the issues above and run validation again.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

