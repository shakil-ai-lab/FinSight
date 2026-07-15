# ADR-008 — Evidence-First Architecture

## Status

Proposed

## Context

While formalizing the earlier decisions, one architectural principle remains unstated: every piece of generated output should be traceable back to the source evidence it came from. Without this rule, facts, insights, and recommendations risk drifting away from what the underlying documents actually support.

## Decision

Every fact, insight, recommendation, and report element must be traceable to one or more pieces of evidence from the source documents.

This principle is a non-negotiable rule throughout FinSight.

Examples:

- `FinancialSnapshot.Revenue` → links to the filing section and table.
- `RiskAssessment` → links to the exact Risk Factors paragraph.
- `ConsistencyReport` → links to both the transcript quote and the filing evidence.
- `MaterialityAssessment` → references the underlying facts and analyses it was derived from.
- `AnalystBrief` → contains only information that can be traced back through this evidence chain.

## Consequences

### Benefits

- Full traceability from conclusion to source
- Stronger auditability for regulated/financial use cases
- Easier fact-checking and dispute resolution
- Reinforces the Facts vs Insights separation established in ADR-006

### Trade-off

- Every capability must carry evidence references through its data model, adding implementation overhead.

This trade-off is acceptable given FinSight's need for defensible, source-backed analysis.
