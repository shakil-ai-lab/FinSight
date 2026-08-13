from __future__ import annotations

from app.application.ports.company_resolution_port import (
    CompanyResolutionPort,
)
from app.application.ports.filing_discovery_port import (
    FilingDiscoveryPort,
)
from app.domain.company import AvailableFilings


class FilingDiscoveryService:
    """
    Application service responsible for discovering available
    financial filings for a company.
    """

    def __init__(
        self,
        company_resolver: CompanyResolutionPort,
        filing_discovery: FilingDiscoveryPort,
    ) -> None:
        self._company_resolver = company_resolver
        self._filing_discovery = filing_discovery

    def discover(
        self,
        company: str,
    ) -> AvailableFilings:
        """
        Resolve the company and discover its available filings.
        """

        resolved_company = self._company_resolver.resolve(
            company,
        )

        return self._filing_discovery.discover(
            resolved_company,
        )