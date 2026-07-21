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

from app.infrastructure.parsing import SECDocumentParser

from app.domain.analysis import AnalysisRequest, AnalysisType



def main():

    planning_service = PlanningService()

    acquisition_service = DocumentAcquisitionService(
        filing_provider=SECFilingProvider(SECClient()),
        transcript_provider=EarningsTranscriptProvider(),
    )

    extraction_service = KnowledgeExtractionService(
        parser=SECDocumentParser()
    )

    request = AnalysisRequest(
    company="Apple",
    ticker="AAPL",
    analysis_type=AnalysisType.ANNUAL,
    fiscal_year=2024,
)

    plan = planning_service.plan(request)

    bundle = acquisition_service.acquire(plan)

    knowledge = extraction_service.extract(bundle)

    print("=" * 80)
    print("Knowledge Extraction Test")
    print("=" * 80)

    print(f"Documents Parsed : {len(knowledge.parsed_documents)}")
    print()
    print(knowledge.parsed_documents[0][:1000])


if __name__ == "__main__":
    main()