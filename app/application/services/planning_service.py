from __future__ import annotations

from app.domain.analysis import (
    AnalysisPlan,
    AnalysisRequest,
    AnalysisType,
    CapabilityType,
)
from app.domain.documents import DocumentType


class PlanningService:
    """
    Application service responsible for creating an
    AnalysisPlan from an AnalysisRequest.
    """

    def plan(
        self,
        request: AnalysisRequest,
    ) -> AnalysisPlan:

        required_documents: list[DocumentType] = []

        # Use explicitly requested documents if provided.
        if request.include_documents:
            required_documents.extend(request.include_documents)

        else:
            match request.analysis_type:

                case AnalysisType.ANNUAL:
                    required_documents.append(DocumentType.TEN_K)

                case AnalysisType.QUARTERLY:
                    required_documents.append(DocumentType.TEN_Q)

                case AnalysisType.TRANSCRIPT:
                    required_documents.append(DocumentType.EARNINGS_TRANSCRIPT)

                case AnalysisType.COMPREHENSIVE:
                    required_documents.extend(
                        [
                            DocumentType.TEN_K,
                            DocumentType.EARNINGS_TRANSCRIPT,
                        ]
                    )

        capabilities = (
            CapabilityType.DOCUMENT_ACQUISITION,
            CapabilityType.KNOWLEDGE_EXTRACTION,
            CapabilityType.KNOWLEDGE_ANALYSIS,
            CapabilityType.DECISION_SUPPORT,
            CapabilityType.PRESENTATION,
        )

        return AnalysisPlan(
            request=request,
            required_documents=tuple(required_documents),
            capabilities=capabilities,
            description=f"{request.company} financial analysis",
        )