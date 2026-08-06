from __future__ import annotations

from app.application.exceptions.company_not_found import CompanyNotFoundError
from app.application.ports.company_resolution_port import CompanyResolutionPort
from app.domain.company.company import Company
from app.infrastructure.document_sources.sec.sec_client import SECClient


class SECCompanyProvider(CompanyResolutionPort):
    """
    Resolves companies using the SEC company tickers dataset.
    """

    def __init__(
        self,
        client: SECClient,
    ) -> None:
        self._client = client

    def resolve(
        self,
        company: str,
    ) -> Company:

        company = company.strip().lower()

        companies = self._client.get_company_tickers()

        for item in companies.values():

            title = item["title"].strip()
            ticker = item["ticker"].strip()

            if (
                company == ticker.lower()
                or company in title.lower()
            ):
                return Company(
                    name=title,
                    ticker=ticker,
                    cik=str(item["cik_str"]).zfill(10),
                )

        raise CompanyNotFoundError(
            f"Unable to resolve company '{company}'."
        )