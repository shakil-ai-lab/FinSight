from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from .document import SourceDocument


@dataclass(slots=True, frozen=True)
class DocumentBundle:
    """
    Represents the complete collection of source documents
    acquired for a single analysis.

    Purpose
    -------
    Groups all evidence required before knowledge extraction
    begins.

    Created By
    ----------
    Document Acquisition Capability

    Consumed By
    -----------
    - Knowledge Extraction
    - Analysis State
    """

    documents: tuple[SourceDocument, ...] = field(default_factory=tuple)

    created_at: datetime = field(default_factory=datetime.utcnow)