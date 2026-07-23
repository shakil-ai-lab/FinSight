from __future__ import annotations

from app.application.models import (
    ExtractedKnowledge,
    ParsedDocument,
)
from app.application.ports import KnowledgeExtractor

from app.infrastructure.llm.gemini import GeminiClient

from .knowledge_extraction_prompt import (
    KnowledgeExtractionPrompt,
)
from .response_parser import ResponseParser
from .extracted_knowledge_mapper import (
    ExtractedKnowledgeMapper,
)


class GeminiKnowledgeExtractor(KnowledgeExtractor):
    """
    Gemini implementation of the KnowledgeExtractor port.

    Responsibility
    --------------
    Orchestrates the complete knowledge extraction pipeline.

        ParsedDocument
              │
              ▼
        KnowledgeExtractionPrompt
              │
              ▼
          GeminiClient
              │
              ▼
        ResponseParser
              │
              ▼
      ExtractedKnowledgeMapper
              │
              ▼
      ExtractedKnowledge

    This class contains no parsing, mapping or prompt
    construction logic. It only coordinates the workflow.
    """

    def __init__(
        self,
        client: GeminiClient,
        prompt: KnowledgeExtractionPrompt,
        response_parser: ResponseParser,
        mapper: ExtractedKnowledgeMapper,
    ) -> None:
        self._client = client
        self._prompt = prompt
        self._response_parser = response_parser
        self._mapper = mapper

    def extract(
        self,
        document: ParsedDocument,
    ) -> ExtractedKnowledge:
        """
        Extract structured financial knowledge from a
        parsed SEC document.
        """

        prompt = self._prompt.build(document)

        response = self._client.generate(prompt)

        parsed_response = self._response_parser.parse(
            response
        )

        return self._mapper.map(
            parsed_response
        )