from app.application.services.document_acquisition_service import (
    DocumentAcquisitionService,
)
from app.domain.analysis import (
    AnalysisPlan,
    AnalysisRequest,
    AnalysisType,
)
from app.domain.documents import DocumentType

from app.infrastructure.document_sources.sec.sec_client import SECClient
from app.infrastructure.document_sources.sec.sec_filing_provider import (
    SECFilingProvider,
)
from app.infrastructure.transcripts.earnings_transcript_provider import (
    EarningsTranscriptProvider,
)


def main() -> None:
    request = AnalysisRequest(
        company="Apple",
        ticker="AAPL",
        analysis_type=AnalysisType.ANNUAL,
        fiscal_year=2024,
    )

    plan = AnalysisPlan(
        request=request,
        required_documents=(
            DocumentType.TEN_K,
        ),
    )

    client = SECClient(
        user_agent="FinSight/1.0 sanjaralap@gmail.com",
    )

    filing_provider = SECFilingProvider(client)
    transcript_provider = EarningsTranscriptProvider()

    service = DocumentAcquisitionService(
        filing_provider=filing_provider,
        transcript_provider=transcript_provider,
    )

    bundle = service.acquire(plan)

    print("=" * 80)
    print("Document Acquisition Service Test")
    print("=" * 80)

    print(f"Documents acquired : {len(bundle.documents)}")
    print()

    for document in bundle.documents:
        print(f"Company         : {document.company}")
        print(f"Type            : {document.document_type.value}")
        print(f"Source          : {document.source.value}")
        print(f"Content Length  : {len(document.content):,}")
        print("-" * 80)


if __name__ == "__main__":
    main()