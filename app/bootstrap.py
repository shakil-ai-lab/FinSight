from __future__ import annotations

from app.infrastructure.transcripts.earnings_transcript_provider import (
    EarningsTranscriptProvider,
)

from app.infrastructure.llm.knowledge_extraction.knowledge_extraction_prompt import (
    KnowledgeExtractionPrompt,
)
from app.infrastructure.llm.knowledge_extraction.response_parser import (
    ResponseParser as KnowledgeExtractionResponseParser,
)
from app.infrastructure.llm.knowledge_extraction.extracted_knowledge_mapper import (
    ExtractedKnowledgeMapper,
)

from app.infrastructure.llm.knowledge_analysis.analysis_prompt import (
    AnalysisPrompt,
)
from app.infrastructure.llm.knowledge_analysis.response_parser import (
    ResponseParser as KnowledgeAnalysisResponseParser,
)
from app.infrastructure.llm.knowledge_analysis.analysis_mapper import (
    AnalysisMapper,
)

from app.infrastructure.llm.decision_support.decision_support_prompt import (
    DecisionSupportPrompt,
)
from app.infrastructure.llm.decision_support.response_parser import (
    ResponseParser as DecisionSupportResponseParser,
)
from app.infrastructure.llm.decision_support.decision_support_mapper import (
    DecisionSupportMapper,
)

from app.application.orchestrators import AnalysisOrchestrator
from app.application.services import (
    DecisionSupportService,
    DocumentAcquisitionService,
    KnowledgeAnalysisService,
    KnowledgeExtractionService,
    PlanningService,
    PresentationService,
)

from app.infrastructure.document_sources.sec.sec_client import SECClient
from app.infrastructure.document_sources.sec.sec_filing_provider import (
    SECFilingProvider,
)
from app.infrastructure.parsing.sec_document_parser import SECDocumentParser

from app.infrastructure.llm.gemini.gemini_client import GeminiClient

from app.infrastructure.llm.knowledge_extraction.gemini_knowledge_extractor import (
    GeminiKnowledgeExtractor,
)
from app.infrastructure.llm.knowledge_analysis.gemini_knowledge_analyzer import (
    GeminiKnowledgeAnalyzer,
)
from app.infrastructure.llm.decision_support.gemini_decision_support_engine import (
    GeminiDecisionSupportEngine,
)
from app.infrastructure.llm.presentation.simple_presentation_engine import (
    SimplePresentationEngine,
)


def build_analysis_orchestrator() -> AnalysisOrchestrator:
    """
    Build the complete FinSight dependency graph.

    This is the application's Composition Root.

    Responsibilities:
        - Instantiate infrastructure components.
        - Wire application services.
        - Construct the AnalysisOrchestrator.

    Contains no business logic.
    """

    # ------------------------------------------------------------------
    # Infrastructure
    # ------------------------------------------------------------------

    sec_client = SECClient()

    filing_provider = SECFilingProvider(
        client=sec_client,
    )

    document_parser = SECDocumentParser()

    gemini_client = GeminiClient()

    # ------------------------------------------------------------
    # Knowledge Extraction
    # ------------------------------------------------------------

    knowledge_extraction_prompt = KnowledgeExtractionPrompt()

    knowledge_extraction_parser = (
        KnowledgeExtractionResponseParser()
    )

    knowledge_extraction_mapper = (
        ExtractedKnowledgeMapper()
    )

    knowledge_extractor = GeminiKnowledgeExtractor(
        client=gemini_client,
        prompt=knowledge_extraction_prompt,
        response_parser=knowledge_extraction_parser,
        mapper=knowledge_extraction_mapper,
    )

    # ------------------------------------------------------------
    # Knowledge Analysis
    # ------------------------------------------------------------

    analysis_prompt = AnalysisPrompt()

    analysis_parser = (
        KnowledgeAnalysisResponseParser()
    )

    analysis_mapper = AnalysisMapper()

    knowledge_analyzer = GeminiKnowledgeAnalyzer(
        client=gemini_client,
        prompt=analysis_prompt,
        response_parser=analysis_parser,
        mapper=analysis_mapper,
    )

    # ------------------------------------------------------------
    # Decision Support
    # ------------------------------------------------------------

    decision_prompt = DecisionSupportPrompt()

    decision_parser = (
        DecisionSupportResponseParser()
    )

    decision_mapper = DecisionSupportMapper()

    decision_support_engine = GeminiDecisionSupportEngine(
        client=gemini_client,
        prompt_builder=decision_prompt,
        response_parser=decision_parser,
        mapper=decision_mapper,
    )

    # ------------------------------------------------------------
    # Presentation
    # ------------------------------------------------------------

    presentation_engine = SimplePresentationEngine()

    # ------------------------------------------------------------------
    # Application Services
    # ------------------------------------------------------------------

    planning_service = PlanningService()

    transcript_provider = EarningsTranscriptProvider()

    document_acquisition_service = DocumentAcquisitionService(
        filing_provider=filing_provider,
        transcript_provider=transcript_provider,
    )

    knowledge_extraction_service = KnowledgeExtractionService(
        parser=document_parser,
        extractor=knowledge_extractor,
    )
    

    knowledge_analysis_service = KnowledgeAnalysisService(
        analyzer=knowledge_analyzer,
    )

    decision_support_service = DecisionSupportService(
        decision_support_engine=decision_support_engine,
    )

    presentation_service = PresentationService(
        engine=presentation_engine,
    )

    # ------------------------------------------------------------------
    # Orchestrator
    # ------------------------------------------------------------------

    return AnalysisOrchestrator(
        planning_service=planning_service,
        document_acquisition_service=document_acquisition_service,
        knowledge_extraction_service=knowledge_extraction_service,
        knowledge_analysis_service=knowledge_analysis_service,
        decision_support_service=decision_support_service,
        presentation_service=presentation_service,
    )