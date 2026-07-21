from __future__ import annotations

from app.application.models import ExtractedKnowledge
from app.application.ports import (
    DocumentParser,
    KnowledgeExtractor,
)
from app.domain.documents import DocumentBundle


class KnowledgeExtractionService:
    """
    Application service responsible for extracting structured
    knowledge from acquired documents.
    """

    def __init__(
        self,
        parser: DocumentParser,
        extractor: KnowledgeExtractor,
    ):
        self._parser = parser
        self._extractor = extractor

    def extract(
        self,
        documents: DocumentBundle,
    ) -> ExtractedKnowledge:

        if not documents.documents:
            raise ValueError("No documents available for extraction.")

        parsed_document = self._parser.parse(
            documents.documents[0]
        )

        return self._extractor.extract(
            parsed_document
        )