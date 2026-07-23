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
from app.application.exceptions import KnowledgeExtractionError
from app.core.logging import get_logger

logger = get_logger(__name__)


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

        try:
            logger.info("Building extraction prompt.")
            prompt = self._prompt.build(document)

            logger.info("Generating response from Gemini.")
            response = self._client.generate(prompt)

            logger.info("Parsing Gemini response.")
            parsed_response = self._response_parser.parse(
                response
            )

            logger.info("Mapping extracted knowledge.")
            result = self._mapper.map(parsed_response)

            logger.info("Knowledge extraction pipeline completed.")
            return result

        except KnowledgeExtractionError:
            logger.exception(
                "Knowledge extraction failed."
            )
            raise

        except Exception as exc:
            logger.exception(
                "Unexpected error during knowledge extraction."
            )

            raise KnowledgeExtractionError(
                "Knowledge extraction pipeline failed."
            ) from exc