# ADR-001 — Knowledge-Centric Architecture

## Status

Accepted

## Context

FinSight analyzes SEC filings and earnings call transcripts.

A straightforward implementation would build the workflow around documents:

```
10-K
  │
  ▼
Transcript
  │
  ▼
Prompt
  │
  ▼
Summary
```

This approach is common in simple RAG applications.

However, FinSight is not intended to be a document summarizer. Its goal is to behave like a financial analyst by extracting reusable knowledge, performing reasoning, and generating decision support.

Therefore, the architecture should not treat documents as the center of the system.

## Decision

FinSight adopts a Knowledge-Centric Architecture.

Documents are considered evidence sources. The core of the system is structured business knowledge.

The processing pipeline is therefore:

```
Documents
   │
   ▼
Observed Facts
   │
   ▼
Business Knowledge
   │
   ▼
Derived Insights
   │
   ▼
Recommendations
   │
   ▼
Reports
```

Documents are never passed directly between analysis components once structured facts have been extracted.

Analysis components operate on business knowledge rather than raw documents.

## Consequences

### Positive

- Easier testing
- Better explainability
- Easier debugging
- Better reuse
- New analysis capabilities can be added without changing retrieval

### Negative

- More initial design work
- Larger domain model
- More schemas

These costs are acceptable for a production-oriented platform.

## Rationale

Knowledge changes more slowly than prompts.

- Documents change every quarter.
- Reports change every release.
- Business knowledge remains stable.

The architecture should therefore optimize around knowledge.
