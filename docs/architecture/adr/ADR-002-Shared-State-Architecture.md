# ADR-002 — Shared Analysis State

## Status

Accepted

## Context

Many LangGraph examples have nodes passing outputs directly:

```
Retriever
   │
   ▼
Extractor
   │
   ▼
Comparator
```

This creates tight coupling.

- Checkpointing becomes difficult.
- Debugging becomes harder.
- Adding new agents requires modifying existing ones.

## Decision

FinSight will use a single shared Analysis State.

```
Planner
   │
   ▼
Analysis State
   ▲
   │
Retriever
   │
   ▼
Analysis State
   ▲
   │
Extractor
```

Each capability reads from and writes to the state.

Capabilities never communicate directly.

## Consequences

### Advantages

- Loose coupling
- Checkpoint support
- Human interruption
- Replay capability
- Better observability
- Easier testing

### Trade-off

State design becomes more important.

This trade-off is acceptable.
