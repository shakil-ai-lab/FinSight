from __future__ import annotations

from app.application.models import ExtractedKnowledge
from app.application.ports import (
    DocumentParser,
    KnowledgeExtractor,
)
from app.domain.documents import DocumentBundle

from app.application.exceptions import KnowledgeExtractionError

from app.core.logging import get_logger

logger = get_logger(__name__)


class KnowledgeExtractionService:
    """
    Application service responsible for extracting structured
    knowledge from acquired documents.
    """

    def extract(
        self,
        documents: DocumentBundle,
    ) -> ExtractedKnowledge:

        try:

            logger.info("Starting knowledge extraction service.")

            if not documents.documents:
                raise KnowledgeExtractionError(
                    "No documents available for extraction."
                )

            logger.info("Parsing document.")

            parsed_document = self._parser.parse(
                documents.documents[0]
            )

            extract_document = self._extractor.extract(parsed_document)

            logger.info("Knowledge extraction completed successfully.")

            return extract_document

        except KnowledgeExtractionError:
            logger.exception(
                "Knowledge extraction service failed."
            )
            raise