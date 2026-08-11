from __future__ import annotations

from app.application.ports.company_resolution_port import (
    CompanyResolutionPort,
)
from app.application.ports.filing_discovery_port import (
    FilingDiscoveryPort,
)
from app.application.ports.filing_provider import FilingProvider
from app.domain.analysis import AnalysisPlan
from app.domain.documents import (
    DocumentRequest,
    DocumentSource,
    SourceDocument,
)
from app.infrastructure.document_sources.sec.sec_client import SECClient


class SECFilingProvider(FilingProvider):
    """
    Infrastructure implementation of the FilingProvider port.
    """

    def __init__(
        self,
        client: SECClient,
        company_resolver: CompanyResolutionPort,
        filing_discovery: FilingDiscoveryPort,
    ) -> None:
        self._client = client
        self._company_resolver = company_resolver
        self._filing_discovery = filing_discovery

    def get_filing(
        self,
        plan: AnalysisPlan,
        document_request: DocumentRequest,
    ) -> SourceDocument:
        """
        Retrieve the SEC filing specified by the document request.
        """

        request = plan.request

        company = self._company_resolver.resolve(
            request.ticker or request.company,
        )

        available_filings = self._filing_discovery.discover(
            company,
        )

        filing = self._find_matching_filing(
            available_filings,
            document_request,
        )

        url = self._build_filing_url(
            cik=int(company.cik),
            accession_number=filing.accession_number,
            primary_document=filing.primary_document,
        )

        content = self._client.download_document(url)

        return SourceDocument(
            company=request.company,
            document_type=document_request.document_type,
            source=DocumentSource.EDGAR,
            fiscal_year=document_request.fiscal_year,
            fiscal_quarter=document_request.fiscal_quarter,
            filing_date=filing.filing_date,
            content=content,
        )

    @staticmethod
    def _find_matching_filing(
        available_filings,
        document_request: DocumentRequest,
    ):
        """
        Find the filing matching the requested document and fiscal period.
        """

        for filing in available_filings.filings:
            if (
                filing.document_type
                is document_request.document_type
                and filing.fiscal_year
                == document_request.fiscal_year
                and filing.fiscal_quarter
                == document_request.fiscal_quarter
            ):
                return filing

        raise ValueError(
            "No matching filing found for "
            f"{document_request.document_type.value}, "
            f"fiscal year {document_request.fiscal_year}, "
            f"fiscal quarter {document_request.fiscal_quarter}."
        )

    @staticmethod
    def _build_filing_url(
        cik: int,
        accession_number: str,
        primary_document: str,
    ) -> str:
        """
        Build the SEC filing URL.
        """

        accession = accession_number.replace("-", "")

        return (
            f"https://www.sec.gov/Archives/edgar/data/"
            f"{cik}/"
            f"{accession}/"
            f"{primary_document}"
        )