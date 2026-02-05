# Conventions

These rules standardize implementation details and reduce ambiguity for both humans and agents.

All contributions must follow these conventions.

---

## General Philosophy

- keep code boring
- avoid unnecessary abstractions
- prefer clarity over flexibility
- shorter paths are better than layered designs

---

## Naming

### Files
snake_case

### Classes
PascalCase

### Functions
snake_case

### Variables
snake_case

---

## Model Naming

Database models:
- singular nouns
- PascalCase

Example:
Product
Customer
Order

Tables:
- plural snake_case

Example:
products
customers

---

## Schema Naming

Pattern:

<Entity>Read
<Entity>List
<Entity>Response

Examples:
ProductRead
ProductList
CustomerResponse

Do NOT reuse ORM models as schemas.

---

## Router Conventions

### Path style

Plural nouns only:

/products
/customers
/orders

Never:
/getProducts
/productList

---

### Endpoint rules

Allowed:
- GET collection
- GET by id

Forbidden:
- POST
- PUT
- PATCH
- DELETE

API is read-only.

---

### Handler size

Endpoints should be small:

- compose query
- return result

If a function exceeds ~30 lines, refactor into utils.

---

## Database Conventions

- SQLAlchemy ORM only
- no raw SQL unless strictly necessary
- use dependency-injected sessions
- never create global sessions
- always close sessions via dependency

---

## Query Style

Prefer:

- explicit select()
- joinedload/selectinload for relationships
- pagination with limit/offset

Avoid:
- implicit lazy loading in loops (N+1)
- complex dynamic query builders

---

## Imports

Order:

1. standard library
2. third-party
3. local app

No wildcard imports.

---

## Type Safety

- mypy clean
- add type hints for all functions
- avoid Any
- prefer explicit Optional[T]

---

## Formatting

Automatically enforced by:

- Ruff (lint)
- Ruff format

Never manually fight the formatter.

---

## Testing Rules

- pytest required
- integration-first testing
- test real database behavior
- dynamic IDs only
- avoid fragile fixtures

Tests must pass before commit (pre-commit hook).

---

## Error Handling

- use HTTPException
- explicit status codes
- no silent failures
- never swallow exceptions

---

## Logging

- simple logging only
- no heavy frameworks
- useful for debugging only

---

## What NOT to Add

Unless explicitly requested:

- service layers
- repository layers
- dependency injection frameworks
- complex design patterns
- ORMs other than SQLAlchemy
- caching systems
- background jobs
- microservices

Simplicity is intentional.

---

## Agent Rules

When modifying code:

- follow existing structure
- do not create new architectural layers
- keep changes minimal
- respect read-only API constraint
- ensure Ruff, mypy, pytest pass
