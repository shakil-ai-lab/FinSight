from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class FilingMetadata:
    """
    Represents metadata describing an SEC filing.
    """

    accession_number: str
    primary_document: str
    filing_date: date