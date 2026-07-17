from __future__ import annotations

from application.ports import FilingProvider

from domain.analysis import AnalysisPlan
from domain.documents import SourceDocument


class SECFilingProvider(FilingProvider):
    """
    Retrieves SEC filing documents required by an analysis plan.

    This implementation is responsible for coordinating the
    retrieval of SEC filings. The actual communication with
    the SEC EDGAR service will be delegated to a dedicated
    client in a future implementation.
    """

    def get_filing(
        self,
        plan: AnalysisPlan,
    ) -> SourceDocument:
        """
        Retrieve the SEC filing specified by the analysis plan.
        """

        raise NotImplementedError(
            "SEC filing retrieval has not been implemented yet."
        )