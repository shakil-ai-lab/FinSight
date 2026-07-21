from __future__ import annotations

from app.application.models import (
    ExtractedKnowledge,
    ParsedDocument,
)
from app.application.ports import KnowledgeExtractor


class GeminiKnowledgeExtractor(KnowledgeExtractor):
    """
    Gemini implementation of the KnowledgeExtractor port.
    """

    def extract(
        self,
        document: ParsedDocument,
    ) -> ExtractedKnowledge:

        raise NotImplementedError(
            "Gemini knowledge extraction is not implemented yet."
        )