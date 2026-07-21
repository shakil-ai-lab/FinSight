from __future__ import annotations

from abc import ABC, abstractmethod

from app.application.models import ParsedDocument
from app.domain.documents import SourceDocument


class DocumentParser(ABC):
    """
    Parses raw source documents into a structured representation.
    """

    @abstractmethod
    def parse(
        self,
        document: SourceDocument,
    ) -> ParsedDocument:
        raise NotImplementedError