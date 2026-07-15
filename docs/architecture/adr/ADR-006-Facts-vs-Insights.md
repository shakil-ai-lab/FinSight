# ADR-006 — Facts vs Insights

> This is probably the most impactful ADR, as it fundamentally shapes the architecture.

## Status

Accepted

## Context

Many AI systems mix extracted information with generated conclusions.

Example:

```
Revenue = 25B
     │
     ▼
Revenue growth is excellent.
```

The first is objective. The second is interpretation.

Mixing them makes validation difficult.

## Decision

FinSight separates:

```
Observed Facts
     │
     ▼
Business Knowledge
     │
     ▼
Derived Insights
```

- Facts are immutable.
- Insights may evolve.
- Reports are regenerated from insights.

## Consequences

### Benefits

- Traceability
- Explainability
- Re-analysis
- Better testing
- Better auditability
