from __future__ import annotations

from datetime import date

from app.application.ports.filing_discovery_port import FilingDiscoveryPort
from app.domain.company.available_filings import AvailableFilings
from app.domain.company.company import Company
from app.domain.documents import DocumentType, FilingMetadata
from app.domain.fiscal.fiscal_period_resolver import FiscalPeriodResolver

from .sec_client import SECClient


class SECFilingDiscoveryService(FilingDiscoveryPort):
    """
    Discovers available SEC filings for a company.
    """

    def __init__(
        self,
        client: SECClient,
    ) -> None:
        self._client = client

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

        fiscal_year_end = submissions["fiscalYearEnd"]

        fiscal_year_end_month = int(
            fiscal_year_end[:2]
        )

        fiscal_year_end_day = int(
            fiscal_year_end[2:]
        )

        recent = submissions["filings"]["recent"]

        filings: list[FilingMetadata] = []

        for index, form in enumerate(recent["form"]):

            document_type = self._resolve_document_type(form)

            if document_type is None:
                continue

            report_date = self._parse_date(
                recent["reportDate"][index]
            )

            filing_date = self._parse_date(
                recent["filingDate"][index]
            )

            resolved_period = FiscalPeriodResolver.resolve(
                report_date=report_date,
                document_type=document_type,
                fiscal_year_end_month=fiscal_year_end_month,
                fiscal_year_end_day=fiscal_year_end_day,
            )

            filings.append(
                FilingMetadata(
                    accession_number=recent["accessionNumber"][index],
                    primary_document=recent["primaryDocument"][index],
                    document_type=document_type,
                    fiscal_year=resolved_period.fiscal_year,
                    fiscal_quarter=(
                        resolved_period.fiscal_quarter
                    ),
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