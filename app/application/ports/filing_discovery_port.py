from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.company.available_filings import AvailableFilings
from app.domain.company.company import Company


class FilingDiscoveryPort(ABC):
    """
    Contract for discovering available financial filings for a company.
    """

    @abstractmethod
    def discover(
        self,
        company: Company,
    ) -> AvailableFilings:
        """
        Discover available SEC filings for the company.
        """
        raise NotImplementedError