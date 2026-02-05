# ADR 0001 — No services layer

Status: Accepted

Context:
Project is small and analytics-focused.

Decision:
Do not introduce services/repositories layers.

Consequences:
- logic stays in routers/utils
- simpler structure
- less indirection

Agent rules:
- do not create services/
- do not move logic into new layers
