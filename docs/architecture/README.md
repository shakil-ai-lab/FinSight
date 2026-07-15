# FinSight Architecture

This folder documents the architectural decisions behind FinSight — a knowledge-centric financial analysis system built on structured facts, insights, and human-reviewed recommendations rather than raw document summarization.

## Architecture Decision Records (ADRs)

| ADR | Title | Status |
|-----|-------|--------|
| [ADR-001](adr/ADR-001-Knowledge-Centric-Architecture.md) | Knowledge-Centric Architecture | Accepted |
| [ADR-002](adr/ADR-002-Shared-State-Architecture.md) | Shared Analysis State | Accepted |
| [ADR-003](adr/ADR-003-Structured-Domain-Objects.md) | Structured Domain Objects | Accepted |
| [ADR-004](adr/ADR-004-Provider-Abstraction.md) | Provider Abstraction | Accepted |
| [ADR-005](adr/ADR-005-Human-In-The-Loop.md) | Human Review | Accepted |
| [ADR-006](adr/ADR-006-Facts-vs-Insights.md) | Facts vs Insights | Accepted |
| [ADR-007](adr/ADR-007-Capability-Based-Architecture.md) | Capability-Based Architecture | Accepted |
| [ADR-008](adr/ADR-008-Evidence-First-Architecture.md) | Evidence-First Architecture | Proposed |

## What is an ADR?

An Architecture Decision Record captures a single significant architectural decision, the context that led to it, and its consequences (positive and negative). They are kept as a historical log — once accepted, an ADR is not rewritten; a new ADR supersedes it if the decision changes.

## High-Level Pipeline

```
Documents → Observed Facts → Business Knowledge → Derived Insights → Recommendations → Reports
```

Each stage corresponds to decisions made in the ADRs above, particularly ADR-001, ADR-003, and ADR-006.
