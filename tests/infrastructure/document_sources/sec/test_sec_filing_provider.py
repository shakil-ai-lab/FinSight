from datetime import date
from unittest.mock import Mock

from app.domain.analysis import AnalysisPlan, AnalysisRequest, AnalysisType
from app.domain.company import Company
from app.domain.documents import DocumentRequest, DocumentType, FilingMetadata
from app.domain.fiscal import FiscalQuarter
from app.infrastructure.document_sources.sec.sec_filing_provider import (
    SECFilingProvider,
)


def test_get_filing_retrieves_matching_filing():
    client = Mock()
    company_resolver = Mock()
    filing_discovery = Mock()

    company = Company(
        name="Apple Inc.",
        ticker="AAPL",
        cik="0000320193",
    )

    company_resolver.resolve.return_value = company

    filing = FilingMetadata(
        accession_number="0000320193-25-000001",
        primary_document="aapl-20250927.htm",
        document_type=DocumentType.TEN_Q,
        fiscal_year=2025,
        fiscal_quarter=FiscalQuarter.Q3,
        filing_date=date(2025, 10, 31),
    )

    available_filings = Mock()
    available_filings.filings = [filing]

    filing_discovery.discover.return_value = available_filings
    client.download_document.return_value = "<html>SEC filing</html>"

    provider = SECFilingProvider(
        client=client,
        company_resolver=company_resolver,
        filing_discovery=filing_discovery,
    )

    request = AnalysisRequest(
        company="Apple Inc.",
        ticker="AAPL",
        analysis_type=AnalysisType.QUARTERLY,
        fiscal_year=2025,
        fiscal_quarter=FiscalQuarter.Q3,
    )

    plan = AnalysisPlan(
        request=request,
        required_documents=(DocumentType.TEN_Q,),
        document_requests=(
            DocumentRequest(
                document_type=DocumentType.TEN_Q,
                fiscal_year=2025,
                fiscal_quarter=FiscalQuarter.Q3,
            ),
        ),
        capabilities=(),
        description="Apple Inc. financial analysis",
    )

    document_request = plan.document_requests[0]

    result = provider.get_filing(
        plan=plan,
        document_request=document_request,
    )

    assert result.company == "Apple Inc."
    assert result.document_type is DocumentType.TEN_Q
    assert result.fiscal_year == 2025
    assert result.fiscal_quarter is FiscalQuarter.Q3
    assert result.filing_date == date(2025, 10, 31)
    assert result.content == "<html>SEC filing</html>"

    company_resolver.resolve.assert_called_once_with("AAPL")
    filing_discovery.discover.assert_called_once_with(company)

    client.download_document.assert_called_once_with(
        "https://www.sec.gov/Archives/edgar/data/"
        "320193/"
        "000032019325000001/"
        "aapl-20250927.htm"
    )

def test_get_filing_selects_matching_fiscal_period():
    client = Mock()
    company_resolver = Mock()
    filing_discovery = Mock()

    company = Company(
        name="Apple Inc.",
        ticker="AAPL",
        cik="0000320193",
    )

    company_resolver.resolve.return_value = company

    wrong_filing = FilingMetadata(
        accession_number="wrong",
        primary_document="wrong.htm",
        document_type=DocumentType.TEN_Q,
        fiscal_year=2025,
        fiscal_quarter=FiscalQuarter.Q2,
        filing_date=date(2025, 8, 1),
    )

    correct_filing = FilingMetadata(
        accession_number="correct",
        primary_document="correct.htm",
        document_type=DocumentType.TEN_Q,
        fiscal_year=2025,
        fiscal_quarter=FiscalQuarter.Q3,
        filing_date=date(2025, 10, 31),
    )

    available_filings = Mock()
    available_filings.filings = [
        wrong_filing,
        correct_filing,
    ]

    filing_discovery.discover.return_value = available_filings
    client.download_document.return_value = "content"

    provider = SECFilingProvider(
        client=client,
        company_resolver=company_resolver,
        filing_discovery=filing_discovery,
    )

    request = AnalysisRequest(
        company="Apple Inc.",
        ticker="AAPL",
        analysis_type=AnalysisType.QUARTERLY,
        fiscal_year=2025,
        fiscal_quarter=FiscalQuarter.Q3,
    )

    plan = AnalysisPlan(
        request=request,
        required_documents=(DocumentType.TEN_Q,),
        document_requests=(
            DocumentRequest(
                document_type=DocumentType.TEN_Q,
                fiscal_year=2025,
                fiscal_quarter=FiscalQuarter.Q3,
            ),
        ),
        capabilities=(),
        description="Apple Inc. financial analysis",
    )

    result = provider.get_filing(
        plan=plan,
        document_request=plan.document_requests[0],
    )

    assert result.filing_date == date(2025, 10, 31)
    assert result.content == "content"
    assert "correct" in client.download_document.call_args.args[0]    