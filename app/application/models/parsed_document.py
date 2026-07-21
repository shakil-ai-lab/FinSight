from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ParsedDocument:
    """
    Structured representation of a parsed source document.

    Produced by the DocumentParser before any knowledge extraction
    or LLM processing occurs.
    """

    document_type: str
    text: str