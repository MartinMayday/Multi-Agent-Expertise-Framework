# Demo 04: Plan-Build-Improve (TaskOutput Gates)

This demo demonstrates the sequential chaining pattern using TaskOutput gates.

## The Pattern
Subagents are independent. To maintain context across steps, each step must explicitly retrieve the output file path of the previous step.

## Workflow
1. **Plan**: Generate `plan.yaml`.
2. **Build**: Read `plan.yaml`, implement code, generate `build_report.json`.
3. **Self-Improve**: Read `build_report.json`, update `expertise.yaml`.

```python
# Pseudo-code logic
plan_path = agent.run("/experts:web:plan 'Add login'")
report = agent.run(f"/experts:web:build {plan_path}")
agent.run(f"/experts:web:self-improve {report}")
```
