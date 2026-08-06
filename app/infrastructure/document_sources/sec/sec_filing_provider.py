from __future__ import annotations

from datetime import date

from app.application.ports.filing_provider import FilingProvider
from app.domain.analysis import AnalysisPlan
from app.domain.documents import (
    DocumentRequest,
    DocumentSource,
    DocumentType,
    FilingMetadata,
    SourceDocument,
)

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
        document_request: DocumentRequest,
    ) -> SourceDocument:
        """
        Retrieve the SEC filing specified by the document request.
        """

        request = plan.request

        cik = self._get_company_cik(request.ticker)

        filing = self._get_filing_metadata(
            cik=cik,
            document_request=document_request,
        )

        # ===================== DEBUG =====================
        # print("=" * 60)
        # print(f"Company        : {request.company}")
        # print(f"Ticker         : {request.ticker}")
        # print(f"CIK            : {cik}")
        # print(f"Document Type  : {document_request.document_type.value}")
        # print(f"Fiscal Year    : {document_request.fiscal_year}")
        # print(f"Fiscal Quarter : {document_request.fiscal_quarter}")
        # print(f"Filing Date    : {filing.filing_date}")
        # print(f"Accession No.  : {filing.accession_number}")
        # print(f"Primary Doc    : {filing.primary_document}")
        # print("=" * 60)
        # ================================================

        url = self._build_filing_url(
            cik=cik,
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

        raise ValueError(
            f"Ticker '{ticker}' was not found."
        )

    def _get_filing_metadata(
        self,
        cik: int,
        document_request: DocumentRequest,
    ) -> FilingMetadata:
        """
        Return metadata for the requested SEC filing.
        """

        submissions = self._client.get_company_submissions(cik)

        recent = submissions["filings"]["recent"]

        # print("=" * 100)
        # for i in range(min(10, len(recent["form"]))):
        #     print(
        #         recent["form"][i],
        #         recent["filingDate"][i],
        #         recent["reportDate"][i],
        #         recent["primaryDocument"][i],
        #     )
        # print("=" * 100)

        forms = recent["form"]

        if document_request.document_type is DocumentType.TEN_K:
            target_form = "10-K"

        elif document_request.document_type is DocumentType.TEN_Q:
            target_form = "10-Q"

        else:
            raise ValueError(
                f"Unsupported filing type: "
                f"{document_request.document_type.value}"
            )

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