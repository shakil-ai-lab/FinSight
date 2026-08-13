from __future__ import annotations

from datetime import date

from app.application.ports.filing_discovery_port import FilingDiscoveryPort
from app.domain.company.available_filings import AvailableFilings
from app.domain.company.company import Company
from app.domain.documents import DocumentType, FilingMetadata

from .sec_client import SECClient
from .sec_fiscal_metadata_parser import SECFiscalMetadataParser


class SECFilingDiscoveryService(FilingDiscoveryPort):
    """
    Discovers available SEC filings for a company.

    Fiscal year and fiscal quarter are obtained from the
    authoritative SEC filing XBRL metadata rather than inferred
    from report dates.
    """

    def __init__(
        self,
        client: SECClient,
        fiscal_metadata_parser: SECFiscalMetadataParser,
    ) -> None:
        self._client = client
        self._fiscal_metadata_parser = fiscal_metadata_parser

    def discover(
        self,
        company: Company,
    ) -> AvailableFilings:
        """
        Discover recent 10-K and 10-Q filings for a company.
        """

        submissions = self._client.get_company_submissions(
            int(company.cik)
        )

        recent = submissions["filings"]["recent"]

        filings: list[FilingMetadata] = []

        for index, form in enumerate(recent["form"]):

            document_type = self._resolve_document_type(form)

            if document_type is None:
                continue

            filing_date = self._parse_date(
                recent["filingDate"][index]
            )

            url = self._build_filing_url(
                cik=int(company.cik),
                accession_number=recent["accessionNumber"][index],
                primary_document=recent["primaryDocument"][index],
            )

            content = self._client.download_document(url)

            fiscal_year, fiscal_quarter = (
                self._fiscal_metadata_parser.parse(content)
            )

            filings.append(
                FilingMetadata(
                    accession_number=recent["accessionNumber"][index],
                    primary_document=recent["primaryDocument"][index],
                    document_type=document_type,
                    fiscal_year=fiscal_year,
                    fiscal_quarter=fiscal_quarter,
                    filing_date=filing_date,
                )
            )

        return AvailableFilings(
            company=company,
            filings=filings,
        )

    @staticmethod
    def _resolve_document_type(
        form: str,
    ) -> DocumentType | None:
        if form == "10-K":
            return DocumentType.TEN_K

        if form == "10-Q":
            return DocumentType.TEN_Q

        return None

    @staticmethod
    def _parse_date(
        value: str,
    ) -> date:
        return date.fromisoformat(value)

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
            "https://www.sec.gov/Archives/edgar/data/"
            f"{cik}/"
            f"{accession}/"
            f"{primary_document}"
        )