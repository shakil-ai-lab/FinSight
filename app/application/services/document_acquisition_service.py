from __future__ import annotations

from app.application.ports.filing_provider import FilingProvider
from app.application.ports.transcript_provider import TranscriptProvider
from app.domain.analysis import AnalysisPlan
from app.domain.documents import (
    DocumentBundle,
    DocumentRequest,
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

        documents: list[SourceDocument] = []

        for document_request in plan.document_requests:

            if document_request.document_type in (
                DocumentType.TEN_K,
                DocumentType.TEN_Q,
            ):
                documents.append(
                    self._acquire_filing(
                        plan=plan,
                        document_request=document_request,
                    )
                )

            elif (
                document_request.document_type
                is DocumentType.EARNINGS_TRANSCRIPT
            ):
                documents.append(
                    self._acquire_transcript(
                        plan=plan,
                        document_request=document_request,
                    )
                )

        return DocumentBundle(
            documents=tuple(documents),
        )

    def _acquire_filing(
        self,
        plan: AnalysisPlan,
        document_request: DocumentRequest,
    ) -> SourceDocument:

        return self._filing_provider.get_filing(
            plan=plan,
            document_request=document_request,
        )

    def _acquire_transcript(
        self,
        plan: AnalysisPlan,
        document_request: DocumentRequest,
    ) -> SourceDocument:

        return self._transcript_provider.get_transcript(
            plan=plan,
            document_request=document_request,
        )