from __future__ import annotations

from dataclasses import dataclass

from app.domain.fiscal import FiscalQuarter

from .document import DocumentType


@dataclass(slots=True, frozen=True)
class DocumentRequest:
    """
    Represents a request to acquire a specific financial document.
    """

    document_type: DocumentType
    fiscal_year: int
    fiscal_quarter: FiscalQuarter | None = None