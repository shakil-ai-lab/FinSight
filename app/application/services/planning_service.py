from __future__ import annotations

from app.domain.analysis import (
    AnalysisPlan,
    AnalysisRequest,
    AnalysisType,
    CapabilityType,
)
from app.domain.documents import (
    DocumentRequest,
    DocumentType,
)


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
                    required_documents.append(
                        DocumentType.EARNINGS_TRANSCRIPT
                    )

                case AnalysisType.COMPREHENSIVE:
                    required_documents.extend(
                        [
                            DocumentType.TEN_K,
                            DocumentType.EARNINGS_TRANSCRIPT,
                        ]
                    )

        document_requests = self._build_document_requests(
            request=request,
            required_documents=required_documents,
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
            document_requests=tuple(document_requests),
            capabilities=capabilities,
            description=f"{request.company} financial analysis",
        )

    def _build_document_requests(
        self,
        request: AnalysisRequest,
        required_documents: list[DocumentType],
    ) -> list[DocumentRequest]:
        """
        Build acquisition requests for every required document.
        """

        document_requests: list[DocumentRequest] = []

        for document_type in required_documents:
            document_requests.append(
                DocumentRequest(
                    document_type=document_type,
                    fiscal_year=request.fiscal_year,
                    fiscal_quarter=request.fiscal_quarter,
                )
            )

        return document_requests