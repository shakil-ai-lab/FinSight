from datetime import date
from unittest.mock import Mock

from app.domain.company.company import Company
from app.domain.documents import DocumentType
from app.domain.fiscal import FiscalQuarter
from app.infrastructure.document_sources.sec.sec_filing_discovery_service import (
    SECFilingDiscoveryService,
)


class TestSECFilingDiscoveryService:

    def setup_method(self):
        self.client = Mock()
        self.fiscal_metadata_parser = Mock()

        self.company = Company(
            name="Apple Inc.",
            ticker="AAPL",
            cik="0000320193",
        )

        self.client.get_company_submissions.return_value = {
            "fiscalYearEnd": "0928",
            "filings": {
                "recent": {
                    "form": [
                        "10-Q",
                        "10-K",
                        "8-K",
                    ],
                    "accessionNumber": [
                        "0000320193-25-000008",
                        "0000320193-24-000073",
                        "0000320193-25-000009",
                    ],
                    "primaryDocument": [
                        "aapl-20241228.htm",
                        "aapl-20240928.htm",
                        "aapl-20250115.htm",
                    ],
                    "filingDate": [
                        "2025-01-30",
                        "2024-11-01",
                        "2025-01-15",
                    ],
                    "reportDate": [
                        "2024-12-28",
                        "2024-09-28",
                        "2025-01-15",
                    ],
                }
            },
        }

        self.client.download_document.side_effect = [
            "<html>10-Q filing</html>",
            "<html>10-K filing</html>",
        ]

        self.fiscal_metadata_parser.parse.side_effect = [
            (2025, FiscalQuarter.Q1),
            (2024, None),
        ]

        self.service = SECFilingDiscoveryService(
            client=self.client,
            fiscal_metadata_parser=self.fiscal_metadata_parser,
        )

    def test_discover_returns_available_filings(self):
        result = self.service.discover(self.company)

        assert result.company == self.company
        assert len(result.filings) == 2

    def test_discover_only_includes_supported_sec_forms(self):
        result = self.service.discover(self.company)

        document_types = [
            filing.document_type
            for filing in result.filings
        ]

        assert document_types == [
            DocumentType.TEN_Q,
            DocumentType.TEN_K,
        ]

    def test_discover_resolves_quarterly_fiscal_period_from_sec_metadata(
        self,
    ):
        result = self.service.discover(self.company)

        filing = result.filings[0]

        assert filing.document_type is DocumentType.TEN_Q
        assert filing.fiscal_year == 2025
        assert filing.fiscal_quarter is FiscalQuarter.Q1

    def test_discover_resolves_annual_fiscal_period_from_sec_metadata(
        self,
    ):
        result = self.service.discover(self.company)

        filing = result.filings[1]

        assert filing.document_type is DocumentType.TEN_K
        assert filing.fiscal_year == 2024
        assert filing.fiscal_quarter is None

    def test_discover_preserves_accession_number(self):
        result = self.service.discover(self.company)

        filing = result.filings[0]

        assert filing.accession_number == "0000320193-25-000008"

    def test_discover_preserves_primary_document(self):
        result = self.service.discover(self.company)

        filing = result.filings[0]

        assert filing.primary_document == "aapl-20241228.htm"

    def test_discover_preserves_filing_date(self):
        result = self.service.discover(self.company)

        filing = result.filings[0]

        assert filing.filing_date == date(2025, 1, 30)

    def test_discover_requests_submissions_using_company_cik(self):
        self.service.discover(self.company)

        self.client.get_company_submissions.assert_called_once_with(
            320193
        )

    def test_discover_downloads_supported_filing_documents(self):
        self.service.discover(self.company)

        assert self.client.download_document.call_count == 2

    def test_discover_uses_sec_fiscal_metadata_parser(self):
        self.service.discover(self.company)

        assert self.fiscal_metadata_parser.parse.call_count == 2

        self.fiscal_metadata_parser.parse.assert_any_call(
            "<html>10-Q filing</html>"
        )

        self.fiscal_metadata_parser.parse.assert_any_call(
            "<html>10-K filing</html>"
        )

    def test_discover_builds_correct_sec_filing_urls(self):
        self.service.discover(self.company)

        calls = self.client.download_document.call_args_list

        assert calls[0].args[0] == (
            "https://www.sec.gov/Archives/edgar/data/"
            "320193/"
            "000032019325000008/"
            "aapl-20241228.htm"
        )

        assert calls[1].args[0] == (
            "https://www.sec.gov/Archives/edgar/data/"
            "320193/"
            "000032019324000073/"
            "aapl-20240928.htm"
        )

    def test_discover_empty_filings_returns_empty_available_filings(self):
        self.client.get_company_submissions.return_value = {
            "fiscalYearEnd": "0928",
            "filings": {
                "recent": {
                    "form": [],
                    "accessionNumber": [],
                    "primaryDocument": [],
                    "filingDate": [],
                    "reportDate": [],
                }
            },
        }

        result = self.service.discover(self.company)

        assert result.company == self.company
        assert result.filings == []

        self.client.download_document.assert_not_called()
        self.fiscal_metadata_parser.parse.assert_not_called()