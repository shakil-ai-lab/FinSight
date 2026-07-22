from __future__ import annotations

from app.infrastructure.llm.gemini import GeminiClient
from .knowledge_extraction_prompt import KnowledgeExtractionPrompt

from app.application.models import (
    ExtractedKnowledge,
    ParsedDocument,
)
from app.application.ports import KnowledgeExtractor


class GeminiKnowledgeExtractor(KnowledgeExtractor):
    """
    Gemini implementation of the KnowledgeExtractor port.
    """

    def __init__(
        self,
        client: GeminiClient,
        prompt_builder: KnowledgeExtractionPrompt,
    ):
        self._client = client
        self._prompt_builder = prompt_builder

    def extract(
        self,
        document: ParsedDocument,
    ) -> ExtractedKnowledge:

        prompt = self._prompt_builder.build(document)

        response = self._client.generate(prompt)

        print(response)

        raise NotImplementedError(
            "Knowledge mapping not implemented."
        )