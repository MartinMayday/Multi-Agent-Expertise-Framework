# Staging Area for Tool Outputs

## Purpose

This directory is for **machine-generated outputs** from execution tools, workflows, and automated processes. Unlike `review-approval/`, this area is for intermediate outputs that may not need human review before use.

## Structure

```
staging/
├── README.md              # This file
└── out/                  # Tool outputs, generated files, logs
    ├── generated/        # Generated artifacts
    ├── logs/            # Execution logs
    └── temp/            # Temporary files
```

## Usage

- **Execution tools** write outputs here
- **Workflows** stage intermediate results here
- **Eval/metrics** write results here
- **Test outputs** can be written here

## Promotion

Files in `staging/out/` can be:
- Used directly by other tools (no promotion needed)
- Promoted to canonical locations via `review-approval/` workflow if they become permanent artifacts
- Cleaned up automatically after workflow completion

## Difference from review-approval/

- `review-approval/`: Human-reviewed changes that will become part of the canonical repo
- `staging/`: Machine outputs that may be temporary or used as-is by tools

