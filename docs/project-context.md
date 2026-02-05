# Project Context

Operational facts and constraints for this repository.

## Stack

- FastAPI
- SQLAlchemy ORM
- PostgreSQL (Neon)
- Alembic migrations
- Ruff (lint/format)
- mypy (types)
- pytest (integration tests)

## Architecture

- Analytics-only API
- Read-only endpoints (no create/update/delete)
- No runtime AI features
- Development-time agent only

## Data model rules

- SQLAlchemy models define database schema only
- Pydantic schemas define API validation/serialization only
- Do not mix responsibilities

## Database rules

- PostgreSQL hosted on Neon
- All DB access through SessionLocal
- Session injected via dependency (get_db)
- Avoid connection leaks
- No raw SQL (ORM only)

## Folder responsibilities

app/routers/      → HTTP endpoints only (read-only for agents)
app/models/       → ORM models (read-only)
app/schemas/      → validation logic allowed
app/utils/        → shared helpers (editable)
app/database.py   → DB session and queries
tests/            → integration and unit tests
docs/             → architecture and decisions

## Behavioral constraints

- API is read-only analytics
- do not add CUD endpoints
- do not introduce services or repositories layers
- keep architecture simple
- prefer utilities over abstractions

## Testing policy

- integration tests hit real Neon dev branch
- tests may query DB to obtain valid IDs dynamically
- avoid hardcoded IDs
- all tests must pass before commit

## CI/CD

- alembic upgrade head executed in CI/CD
- GitHub Actions connects to Neon dev branch
- Ruff + mypy + pytest are mandatory gates

## Known leftovers

- app/services/ may exist but is unused legacy code
- safe to delete or ignore unless authentication is reintroduced

## Health endpoint

- /health performs SELECT 1
- returns 503 on DB failure

## Neon specifics

- ID gaps are normal (sequence behavior)
- database branches are used for testing
