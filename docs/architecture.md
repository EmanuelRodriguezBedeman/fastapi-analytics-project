# Architecture

This document defines the structural design of the project and strict boundaries between components.

The system is intentionally simple.  
Avoid additional layers or patterns unless absolutely required.

---

## High-Level Style

Monolith REST API.

Pattern:

Router → Schema → ORM → Database

No service layer.  
No repository layer.  
No domain layer.

Reason: analytics-only read operations do not justify extra abstractions.

---

## Request Flow

HTTP Request
  ↓
Router (FastAPI endpoint)
  ↓
DB session (dependency injection)
  ↓
SQLAlchemy query
  ↓
ORM models
  ↓
Pydantic schema serialization
  ↓
JSON response

Routers must not contain business logic beyond simple query composition.

---

## Folder Responsibilities

### app/routers/
Purpose: HTTP layer only

Contains:
- route definitions
- query parameters
- dependency injection
- response models

Must NOT contain:
- business logic
- data transformations
- database setup
- complex calculations

---

### app/models/
Purpose: Database schema mapping

Contains:
- SQLAlchemy ORM models
- relationships
- table definitions

Rules:
- mirror database structure only
- no API logic
- no validation logic
- no Pydantic

Models represent persistence, not transport.

---

### app/schemas/
Purpose: API contract

Contains:
- Pydantic models for validation/serialization

Used for:
- response_model
- filtering fields
- type guarantees
- OpenAPI documentation

Rules:
- never import SQLAlchemy here
- schemas are not DB objects

Schemas represent transport, not persistence.

---

### app/utils/
Purpose: shared utilities

Examples:
- dependencies (get_db)
- pagination helpers
- common filters
- small pure helpers

Rules:
- must remain framework-agnostic when possible
- avoid hidden side effects

---

### app/database.py
Purpose: database configuration

Contains:
- engine
- SessionLocal
- Base
- connection setup

Single source of truth for DB access.

No queries should be defined here.

---

### tests/
Purpose: integration + unit testing

Rules:
- tests hit Neon dev branch
- tests must not mock DB by default
- prefer real queries
- dynamic IDs only (no hardcoded primary keys)

---

### scripts/
Purpose: local utilities only

Examples:
- data seeding
- table inspection
- playground tools

Never imported by the application.

---

## Architectural Constraints

The API is:

- read-only
- analytics focused
- stateless

Therefore:

Do NOT introduce:
- create/update/delete endpoints
- authentication systems
- background workers
- caching layers
- service/repository abstractions
- microservices
- message brokers

If any of the above becomes necessary, redesign explicitly before implementation.

---

## Dependency Direction

Allowed:

routers → schemas
routers → models
routers → utils
schemas → (nothing else)
models → (nothing else)
utils → standard libs only

Forbidden:

models → routers
schemas → models
circular imports

---

## Design Principles

- explicit over clever
- fewer files over more layers
- simple SQLAlchemy queries over abstraction
- readability over patterns
- minimize magic
