from __future__ import annotations

from app.infrastructure.llm.gemini import GeminiClient

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
):
        self._client = client

    def extract(
    self,
    document: ParsedDocument,
) -> ExtractedKnowledge:

        prompt = f"""
    You are a financial analyst.

    Summarize the following SEC filing.

    {document.cleaned_text[:10000]}
    """

        response = self._client.generate(prompt)

        print(response)

        raise NotImplementedError(
            "Knowledge mapping not implemented."
        )