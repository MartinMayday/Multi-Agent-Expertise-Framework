# Demo 05: Expertise Validation

This demo shows why the codebase is the ultimate source of truth.

## Scenario
The `expertise.yaml` claims the database uses Postgres, but the codebase shows a migration to Supabase.

## Workflow
1. Agent reads `expertise.yaml`.
2. Agent runs `grep` on `docker-compose.yml`.
3. Agent identifies discrepancy.
4. Agent updates expertise and answers correctly.
