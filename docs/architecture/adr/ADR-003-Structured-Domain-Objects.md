# ADR-003 — Structured Domain Objects

## Status

Accepted

## Context

LLMs naturally return text.

Text is difficult to validate, compare, and reuse.

Multiple downstream capabilities require reliable structured information.

## Decision

Every capability boundary must exchange structured business objects.

Examples:

- `FinancialSnapshot`
- `RiskAssessment`
- `ConsistencyReport`
- `MaterialityAssessment`
- `AnalystBrief`

Plain text is considered presentation only.

## Consequences

### Benefits

- Strong typing
- Validation
- Easier testing
- Versioning
- Better APIs
