from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.analysis import AnalysisPlan
from app.domain.documents import (
    DocumentRequest,
    SourceDocument,
)


class TranscriptProvider(ABC):
    """
    Defines the contract for retrieving earnings call transcripts.
    """

    @abstractmethod
    def get_transcript(
        self,
        plan: AnalysisPlan,
        document_request: DocumentRequest,
    ) -> SourceDocument:
        """
        Retrieve the transcript specified by the document request.
        """
        raise NotImplementedError