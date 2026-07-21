from __future__ import annotations

from app.domain.analysis import AnalysisRequest
from app.domain.presentation import AnalystBrief

from app.application.services import (
    PlanningService,
    DocumentAcquisitionService,
    KnowledgeExtractionService,
    KnowledgeAnalysisService,
    DecisionSupportService,
    PresentationService,
)


class AnalysisOrchestrator:
    """
    Coordinates the complete financial analysis workflow.

    The orchestrator is responsible only for coordinating
    application services. It contains no business logic.
    """

    def __init__(
        self,
        planning_service: PlanningService,
        document_acquisition_service: DocumentAcquisitionService,
        knowledge_extraction_service: KnowledgeExtractionService,
        knowledge_analysis_service: KnowledgeAnalysisService,
        decision_support_service: DecisionSupportService,
        presentation_service: PresentationService,
    ) -> None:
        self._planning_service = planning_service
        self._document_acquisition_service = document_acquisition_service
        self._knowledge_extraction_service = knowledge_extraction_service
        self._knowledge_analysis_service = knowledge_analysis_service
        self._decision_support_service = decision_support_service
        self._presentation_service = presentation_service

    def analyze(
        self,
        request: AnalysisRequest,
    ) -> AnalystBrief:
        """
        Execute the complete financial analysis workflow.
        """

        plan = self._planning_service.plan(request)

        documents = self._document_acquisition_service.acquire(plan)

        knowledge = self._knowledge_extraction_service.extract(documents)

        insights = self._knowledge_analysis_service.analyze(knowledge)

        decision = self._decision_support_service.assess(insights)

        brief = self._presentation_service.present(decision)

        return brief