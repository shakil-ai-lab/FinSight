from __future__ import annotations

from abc import ABC, abstractmethod

from domain.analysis import AnalysisPlan
from domain.documents import DocumentBundle


class DocumentAcquisitionService(ABC):
    """
    Defines the application capability responsible for
    acquiring all source documents required for analysis.
    """

    @abstractmethod
    def acquire(
        self,
        plan: AnalysisPlan,
    ) -> DocumentBundle:
        """
        Acquire the documents required by the analysis plan.

        Returns
        -------
        DocumentBundle
            The complete collection of source documents.
        """
        raise NotImplementedError