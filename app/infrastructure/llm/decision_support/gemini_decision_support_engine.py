from __future__ import annotations

from app.application.models.analysis_insights import AnalysisInsights
from app.application.models.decision_result import DecisionResult
from app.application.models.extracted_knowledge import ExtractedKnowledge
from app.application.ports.decision_support_engine import DecisionSupportEngine
from app.core.logging import get_logger
from app.infrastructure.llm.gemini.gemini_client import GeminiClient

from .decision_support_mapper import DecisionSupportMapper
from .decision_support_prompt import DecisionSupportPrompt
from .response_parser import ResponseParser


logger = get_logger(__name__)


class GeminiDecisionSupportEngine(DecisionSupportEngine):
    """
    Gemini implementation of the Decision Support capability.
    """

    def __init__(
        self,
        client: GeminiClient,
        prompt_builder: DecisionSupportPrompt,
        response_parser: ResponseParser,
        mapper: DecisionSupportMapper,
    ) -> None:
        self._client = client
        self._prompt_builder = prompt_builder
        self._response_parser = response_parser
        self._mapper = mapper

    def generate(
        self,
        knowledge: ExtractedKnowledge,
        insights: AnalysisInsights,
    ) -> DecisionResult:

        logger.info("Building Decision Support prompt.")

        prompt = self._prompt_builder.build(
            knowledge=knowledge,
            insights=insights,
        )

        logger.info("Sending Decision Support request to Gemini.")

        response = self._client.generate(prompt)

        logger.info("Parsing Decision Support response.")

        parsed = self._response_parser.parse(response)

        logger.info("Mapping Decision Support result.")

        return self._mapper.map(
            response=parsed,
            knowledge=knowledge,
            insights=insights,
        )