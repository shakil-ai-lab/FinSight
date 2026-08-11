from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from app.domain.fiscal import FiscalQuarter

from .document_type import DocumentType


@dataclass(frozen=True, slots=True)
class FilingMetadata:
    """
    Represents metadata describing an SEC filing.
    """

    accession_number: str
    primary_document: str
    document_type: DocumentType
    fiscal_year: int
    fiscal_quarter: FiscalQuarter | None
    filing_date: date