# ADR-007 — Capability-Based Architecture

> This is another architectural improvement over the original proposal.

## Status

Accepted

## Context

The initial proposal organizes the system around agents.

However, agents are implementation choices. Business capabilities are stable.

## Decision

FinSight is organized around business capabilities.

```
Planning
   │
   ▼
Document Acquisition
   │
   ▼
Knowledge Extraction
   │
   ▼
Knowledge Analysis
   │
   ▼
Decision Support
   │
   ▼
Presentation
```

Individual agents may change internally without affecting the overall architecture.

## Consequences

### Benefits

- Easier scaling
- Easier refactoring
- Better separation of concerns
- Future-proof architecture
