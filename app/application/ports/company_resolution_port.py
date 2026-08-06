from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.company.company import Company


class CompanyResolutionPort(ABC):
    """
    Contract for resolving a company into its canonical identity.
    """

    @abstractmethod
    def resolve(
        self,
        company: str,
    ) -> Company:
        """
        Resolve a company name or ticker.

        Raises:
            CompanyNotFoundError
        """
        raise NotImplementedError