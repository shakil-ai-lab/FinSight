from __future__ import annotations

from app.application.ports.filing_provider import FilingProvider
from app.domain.analysis import AnalysisPlan
from app.domain.documents import (
    DocumentSource,
    DocumentType,
    SourceDocument,
)

from datetime import date
from app.domain.documents import FilingMetadata

from .sec_client import SECClient


class SECFilingProvider(FilingProvider):
    """
    Infrastructure implementation of the FilingProvider port.
    """

    def __init__(self, client: SECClient) -> None:
        self._client = client

    def get_filing(
        self,
        plan: AnalysisPlan,
    ) -> SourceDocument:

        document_type = self._resolve_document_type(plan)

        request = plan.request

        cik = self._get_company_cik(request.ticker)

        filing = self._get_latest_filing_metadata(
            cik,
            document_type,
        )

        url = self._build_filing_url(
            cik=cik,
            accession_number=filing.accession_number,
            primary_document=filing.primary_document,
        )

        content = self._client.download_document(url)

        return SourceDocument(
            company=request.company,
            document_type=document_type,
            source=DocumentSource.EDGAR,
            fiscal_year=request.fiscal_year,
            fiscal_quarter=request.fiscal_quarter,
            filing_date=filing.filing_date,
            content=content,
        )

    
    def _resolve_document_type(
        self,
        plan: AnalysisPlan,
    ) -> DocumentType:

        if DocumentType.TEN_K in plan.required_documents:
            return DocumentType.TEN_K

        if DocumentType.TEN_Q in plan.required_documents:
            return DocumentType.TEN_Q

        raise ValueError(
            "AnalysisPlan does not request an SEC filing."
        )


    def _get_company_cik(
        self,
        ticker: str | None,
    ) -> int:
        """
        Resolve a stock ticker to its SEC CIK.
        """

        if not ticker:
            raise ValueError("Ticker is required.")

        companies = self._client.get_company_tickers()

        ticker = ticker.upper()

        for company in companies.values():

            if company["ticker"].upper() == ticker:
                return company["cik_str"]
                print(company)
                print(f"CIK for ticker '{ticker}': {company['cik_str']}")

        raise ValueError(
            f"Ticker '{ticker}' was not found."
        )

    def _get_latest_filing_metadata(
        self,
        cik: int,
        document_type: DocumentType,
    ) -> dict:
        """
        Return metadata for the latest requested filing.
        """

        submissions = self._client.get_company_submissions(cik)

        recent = submissions["filings"]["recent"]

        forms = recent["form"]

        if document_type is DocumentType.TEN_K:
            target_form = "10-K"
        else:
            target_form = "10-Q"

        for index, form in enumerate(forms):

            if form == target_form:

                return FilingMetadata(
                    accession_number=recent["accessionNumber"][index],
                    primary_document=recent["primaryDocument"][index],
                    filing_date=date.fromisoformat(
                        recent["filingDate"][index]
                    ),
                )

        raise ValueError(
            f"No {target_form} filing found."
        )

    def _build_filing_url(
        self,
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