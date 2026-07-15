# ADR-004 — Provider Abstraction

## Status

Accepted

## Context

Model providers evolve rapidly.

The project currently uses Hugging Face.

Future versions may use Gemini, OpenAI, Claude, or local models.

The application should not depend on a specific provider.

## Decision

Provider selection is configuration-driven.

Example:

```
Primary
   │
   ▼
HuggingFace
   │
   ▼ (Failure)
Gemini
   │
   ▼ (Failure)
OpenAI
```

The remainder of the system interacts only with an abstract LLM interface.

## Consequences

Changing providers should require configuration changes rather than application redesign.
