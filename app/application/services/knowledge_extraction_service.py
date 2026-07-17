from __future__ import annotations

from abc import ABC, abstractmethod

from application.models import ExtractedKnowledge

from domain.documents import DocumentBundle


class KnowledgeExtractionService(ABC):
    """
    Defines the application capability responsible for
    extracting structured business knowledge from documents.
    """

    @abstractmethod
    def extract(
        self,
        documents: DocumentBundle,
    ) -> ExtractedKnowledge:
        """
        Extract structured business knowledge from the
        acquired documents.
        """
        raise NotImplementedError