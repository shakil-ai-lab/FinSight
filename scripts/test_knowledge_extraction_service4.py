from __future__ import annotations

from app.infrastructure.llm.gemini import GeminiClient

from app.application.services import (
    PlanningService,
    DocumentAcquisitionService,
    KnowledgeExtractionService,
)

from app.infrastructure.document_sources.sec import (
    SECClient,
    SECFilingProvider,
)

from app.infrastructure.transcripts import (
    EarningsTranscriptProvider,
)

from app.infrastructure.parsing import (
    SECDocumentParser,
)

from app.infrastructure.llm.knowledge_extractor import (
    GeminiKnowledgeExtractor,
)

from app.domain.analysis import (
    AnalysisRequest,
    AnalysisType,
)


def main() -> None:
    print("=" * 80)
    print("Knowledge Extraction Pipeline Test")
    print("=" * 80)

    # ------------------------------------------------------------------
    # Services
    # ------------------------------------------------------------------
    planning_service = PlanningService()

    acquisition_service = DocumentAcquisitionService(
        filing_provider=SECFilingProvider(SECClient()),
        transcript_provider=EarningsTranscriptProvider(),
    )

    extraction_service = KnowledgeExtractionService(
    parser=SECDocumentParser(),
    extractor=GeminiKnowledgeExtractor(
        GeminiClient()
    ),
)

    # ------------------------------------------------------------------
    # Analysis Request
    # ------------------------------------------------------------------
    request = AnalysisRequest(
        company="Apple",
        ticker="AAPL",
        analysis_type=AnalysisType.ANNUAL,
        fiscal_year=2024,
    )

    # ------------------------------------------------------------------
    # Planning
    # ------------------------------------------------------------------
    print("Creating analysis plan...")
    plan = planning_service.plan(request)

    # ------------------------------------------------------------------
    # Document Acquisition
    # ------------------------------------------------------------------
    print("Acquiring documents...")
    bundle = acquisition_service.acquire(plan)

    print(f"Documents acquired: {len(bundle.documents)}")

    # ------------------------------------------------------------------
    # Knowledge Extraction
    # ------------------------------------------------------------------
    print("Extracting knowledge...")
    extraction_service.extract(bundle)


if __name__ == "__main__":
    main()