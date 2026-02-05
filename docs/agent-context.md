Project conventions for agents:

- No services layer
- No repository pattern
- SQLAlchemy ORM only (no raw SQL)
- Routers handle HTTP only
- DB access centralized in database.py
- Prefer simple utilities over abstractions
- Small diffs preferred
