from app.domain.analysis import (
    AnalysisRequest,
    AnalysisPlan,
    AnalysisType,
)
from app.domain.documents import DocumentType, DocumentSource

from app.infrastructure.document_sources.sec.sec_client import SECClient
from app.infrastructure.document_sources.sec.sec_filing_provider import (
    SECFilingProvider,
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

    provider = SECFilingProvider(client)

    document = provider.get_filing(plan)

    print("=" * 80)
    print("SEC Filing Provider Test")
    print("=" * 80)

    print(f"Company          : {document.company}")
    print(f"Document Type    : {document.document_type.value}")
    print(f"Source           : {document.source.value}")
    print(f"Fiscal Year      : {document.fiscal_year}")
    print(f"Fiscal Quarter   : {document.fiscal_quarter}")
    print(f"Content Length   : {len(document.content):,}")
    print()

    print(document.content[:500])


if __name__ == "__main__":
    main()