from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.analysis import AnalysisPlan
from app.domain.documents import SourceDocument


class TranscriptProvider(ABC):
    """
    Defines the contract for retrieving earnings call
    transcripts from an external source.
    """

    @abstractmethod
    def get_transcript(
        self,
        plan: AnalysisPlan,
    ) -> SourceDocument:
        """
        Retrieve the earnings call transcript required by
        the analysis plan.
        """
        raise NotImplementedError