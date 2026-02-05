This agent operates only at development time inside the IDE.

It may modify code only within the allowed paths below.
If a task requires changes outside these rules, stop and ask the user.

## Editable paths:

- tests/**
- app/utils/**
- app/schemas/**
- app/database.py

## Read-only paths:

- .env
- app/models/**
- app/routers/**
- app/main.py
- app/config.py
- docs/**
- scripts/**
- .github/**
- AGENTS.md
- Dockerfile

## Allowed changes

- bug fixes
- add or update tests
- add validation inside schemas
optimize or fix SQLAlchemy queries and database logic in database.py

- fix lint or type errors

## Forbidden changes

- add or modify endpoints or routers
- change public API behavior
- modify database schema or models
- create migrations
- add dependencies
- rename or move modules
- modify CI/CD, Docker, or infrastructure
- edit configuration files

---

## Tooling gates (mandatory)

Pre-commit hooks enforce Ruff, mypy, and pytest automatically. 
Commits are blocked if any check fails. 
The agent must not bypass these hooks.

All must pass before committing:

- ruff check . --fix
- ruff format .
- mypy app/
- pytest tests/ -v

If any check fails, fix before committing.

---

## Commit policy

- one logical change per commit
- minimal diff only
- avoid large refactors
- do not edit unrelated files

---

## Autonomy

Allowed without asking:
- bug fixes
- test fixes
- internal refactors
- readability improvements

Must ask first:
- new endpoints
- behavior changes
- schema or model changes
- new dependencies
- infrastructure or deployment changes


---

For every task, follow this procedure strictly:

1. Scope
   - Read only the files directly related to the request.
   - Do not scan or modify unrelated modules.

2. Minimal change first
   - Implement the smallest change that solves the problem.
   - Prefer edits over rewrites.

3. Local improvements allowed (same file only)
   You may:
   - simplify logic
   - remove dead code
   - improve naming
   - extract small helpers
   - add validation
   - add or update tests
   - fix lint or typing issues

4. Do NOT expand scope
   Do not:
   - refactor other files
   - reorganize folders
   - introduce new abstractions or patterns
   - modify architecture
   - perform large cleanups

5. Safety checks
   - run Ruff
   - run mypy
   - run pytest
   - fix failures before committing

6. Stop after success
   - once tests pass and the task is solved, stop
   - do not perform extra improvements

---

## General rules

- keep changes small and reviewable
- modify only editable paths
- prefer minimal edits over rewrites
- add comments only when logic is non-obvious
