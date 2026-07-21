from __future__ import annotations

from abc import ABC, abstractmethod

from app.application.models import (
    ExtractedKnowledge,
    ParsedDocument,
)


class KnowledgeExtractor(ABC):
    """
    Application port responsible for converting parsed documents
    into structured financial knowledge.
    """

    @abstractmethod
    def extract(
        self,
        document: ParsedDocument,
    ) -> ExtractedKnowledge:
        """
        Extract structured knowledge from a parsed document.
        """
        raise NotImplementedError