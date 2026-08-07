from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.company import Company
from app.domain.documents.filing_metadata import FilingMetadata


@dataclass(frozen=True, slots=True)
class AvailableFilings:
    """
    Represents the SEC filings available for a company.
    """

    company: Company
    filings: list[FilingMetadata] = field(default_factory=list)