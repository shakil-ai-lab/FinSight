from __future__ import annotations

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
        sec_client=sec_client,
    )

    document_parser = SECDocumentParser()

    gemini_client = GeminiClient()

    knowledge_extractor = GeminiKnowledgeExtractor(
        client=gemini_client,
    )

    knowledge_analyzer = GeminiKnowledgeAnalyzer(
        client=gemini_client,
    )

    decision_support_engine = GeminiDecisionSupportEngine(
        client=gemini_client,
    )

    presentation_engine = SimplePresentationEngine()

    # ------------------------------------------------------------------
    # Application Services
    # ------------------------------------------------------------------

    planning_service = PlanningService()

    document_acquisition_service = DocumentAcquisitionService(
        filing_provider=filing_provider,
        document_parser=document_parser,
    )

    knowledge_extraction_service = KnowledgeExtractionService(
        extractor=knowledge_extractor,
    )

    knowledge_analysis_service = KnowledgeAnalysisService(
        analyzer=knowledge_analyzer,
    )

    decision_support_service = DecisionSupportService(
        engine=decision_support_engine,
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