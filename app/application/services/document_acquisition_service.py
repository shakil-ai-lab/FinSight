from __future__ import annotations

from app.application.ports.filing_provider import FilingProvider
from app.application.ports.transcript_provider import TranscriptProvider
from app.domain.analysis import AnalysisPlan
from app.domain.documents import (
    DocumentBundle,
    DocumentType,
    SourceDocument,
)


class DocumentAcquisitionService:
    """
    Coordinates the acquisition of all documents required for an analysis.

    This service orchestrates the document providers and assembles
    the acquired documents into a DocumentBundle.
    """

    def __init__(
        self,
        filing_provider: FilingProvider,
        transcript_provider: TranscriptProvider,
    ) -> None:
        self._filing_provider = filing_provider
        self._transcript_provider = transcript_provider

    def acquire(
        self,
        plan: AnalysisPlan,
    ) -> DocumentBundle:
        """
        Acquire every document required by the analysis plan.
        """

        documents: list[SourceDocument] = []

        for document_type in plan.required_documents:

            if document_type in (
                DocumentType.TEN_K,
                DocumentType.TEN_Q,
            ):
                documents.append(
                    self._acquire_filing(plan)
                )

            elif document_type is DocumentType.EARNINGS_TRANSCRIPT:
                documents.append(
                    self._acquire_transcript(plan)
                )

        return DocumentBundle(
            documents=tuple(documents),
        )

    def _acquire_filing(
        self,
        plan: AnalysisPlan,
    ) -> SourceDocument:
        """
        Acquire an SEC filing.
        """

        return self._filing_provider.get_filing(plan)

    def _acquire_transcript(
        self,
        plan: AnalysisPlan,
    ) -> SourceDocument:
        """
        Acquire an earnings call transcript.
        """

        return self._transcript_provider.get_transcript(plan)