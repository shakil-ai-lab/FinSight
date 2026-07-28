from __future__ import annotations

from app.application.exceptions.knowledge_analysis import (
    KnowledgeAnalysisError,
)
from app.application.models import (
    AnalysisInsights,
    ExtractedKnowledge,
)
from app.application.ports import KnowledgeAnalyzer
from app.core.logging import get_logger

from ..gemini.gemini_client import GeminiClient
from .analysis_mapper import AnalysisMapper
from .analysis_prompt import AnalysisPrompt
from .response_parser import ResponseParser

logger = get_logger(__name__)


class GeminiKnowledgeAnalyzer(KnowledgeAnalyzer):

    def __init__(
        self,
        client: GeminiClient,
        prompt: AnalysisPrompt,
        response_parser: ResponseParser,
        mapper: AnalysisMapper,
    ) -> None:

        self._client = client
        self._prompt = prompt
        self._parser = response_parser
        self._mapper = mapper

    def analyze(
        self,
        knowledge: ExtractedKnowledge,
    ) -> AnalysisInsights:

        try:

            logger.info("Building analysis prompt.")

            prompt = self._prompt.build(knowledge)

            logger.info("Generating analytical insights.")

            response = self._client.generate(prompt)

            logger.info("Parsing analysis response.")


            parsed = self._parser.parse(response)

            logger.info("Mapping analysis insights.")

            insights = self._mapper.map(
            parsed,
            knowledge,
            )

            logger.info(
                "Knowledge analysis completed."
            )

            return insights

        except Exception as exc:

            logger.exception(
                "Knowledge analysis failed."
            )

            raise KnowledgeAnalysisError(
                "Knowledge analysis failed."
            ) from exc