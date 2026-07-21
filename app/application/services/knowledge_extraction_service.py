from __future__ import annotations

from app.application.models import (
    ExtractedKnowledge,
    ParsedDocument,
)
from app.application.ports import DocumentParser
from app.domain.documents import DocumentBundle


class KnowledgeExtractionService:
    """
    Application service responsible for extracting structured
    knowledge from acquired documents.
    """

    def __init__(
        self,
        parser: DocumentParser,
    ) -> None:
        self._parser = parser

    def extract(
        self,
        documents: DocumentBundle,
    ) -> ExtractedKnowledge:
        
        # print("Before parsing")
        parsed_documents: list[ParsedDocument] = []

        for document in documents.documents:
            # print("Parsing document...")
            parsed_documents.append(
                self._parser.parse(document)
            )

        # Temporary placeholder until the LLM extractor is implemented.
        print(f"Parsed {len(parsed_documents)} document(s).")

        raise NotImplementedError(
            "Knowledge extraction mapping has not yet been implemented."
        )