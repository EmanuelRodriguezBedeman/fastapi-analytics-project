This agent operates only at development time inside the IDE.

It may modify code only within the allowed paths below.
If a task requires changes outside these rules, stop and ask the user.

## Editable paths:

- tests/**
- app/utils/**
- app/schemas/**

## Read-only paths:

- .env
- app/models/**
- app/routers/**
- app/main.py
- app/config.py
- app/database.py
- docs/**
- scripts/**
- .github/**
- AGENTS.md
- Dockerfile

## Allowed changes

- bug fixes
- add or update tests
- add validation inside schemas or services
- optimize existing queries
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

All must pass before committing:

- python -m ruff check . --fix
- python -m ruff format .
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

## General rules

- keep changes small and reviewable
- modify only editable paths
- prefer minimal edits over rewrites
- add comments only when logic is non-obvious
