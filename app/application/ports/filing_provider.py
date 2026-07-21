from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.analysis import AnalysisPlan
from app.domain.documents import SourceDocument


class FilingProvider(ABC):
    """
    Defines the contract for retrieving financial filing
    documents from an external source.
    """

    @abstractmethod
    def get_filing(
        self,
        plan: AnalysisPlan,
    ) -> SourceDocument:
        """
        Retrieve the filing document required by the
        analysis plan.
        """
        raise NotImplementedError