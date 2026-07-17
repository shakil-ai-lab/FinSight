from __future__ import annotations

from app.application.ports.transcript_provider import TranscriptProvider
from app.domain.analysis import AnalysisPlan
from app.domain.documents import SourceDocument


class EarningsTranscriptProvider(TranscriptProvider):
    """
    Infrastructure implementation of the TranscriptProvider port.

    Responsible for retrieving earnings call transcripts from an
    external provider.
    """

    def get_transcript(
        self,
        plan: AnalysisPlan,
    ) -> SourceDocument:
        """
        Retrieve the earnings call transcript described by the
        analysis plan.

        Args:
            plan:
                Analysis plan describing the requested transcript.

        Returns:
            SourceDocument representing the retrieved transcript.

        Raises:
            NotImplementedError:
                Until external API integration is implemented.
        """
        raise NotImplementedError(
            "Transcript retrieval has not been implemented yet."
        )