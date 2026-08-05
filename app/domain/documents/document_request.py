from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .document import DocumentType


@dataclass(slots=True, frozen=True)
class DocumentRequest:
    """
    Represents a request to acquire a specific financial document.

    Purpose
    -------
    Defines the exact document that the Document Acquisition
    capability must retrieve.

    Created By
    ----------
    Planning Capability

    Consumed By
    -----------
    - Document Acquisition Service
    - Filing Provider
    - Transcript Provider

    Notes
    -----
    This object describes *what* document is required.
    It contains no acquisition logic.
    """

    document_type: DocumentType

    fiscal_year: int

    fiscal_quarter: Optional[int] = None