from __future__ import annotations

from app.application.ports.filing_provider import FilingProvider
from app.domain.analysis import AnalysisPlan
from app.domain.documents import (
    DocumentSource,
    DocumentType,
    SourceDocument,
)

from .sec_client import SECClient


class SECFilingProvider(FilingProvider):
    """
    Infrastructure implementation of the FilingProvider port.
    """

    def __init__(self, client: SECClient) -> None:
        self._client = client

    def get_filing(
        self,
        plan: AnalysisPlan,
    ) -> SourceDocument:

        document_type = self._resolve_document_type(plan)

        url = self._get_test_filing_url(document_type)

        content = self._client.download_document(url)

        request = plan.request

        return SourceDocument(
            company=request.company,
            document_type=document_type,
            source=DocumentSource.EDGAR,
            fiscal_year=request.fiscal_year,
            fiscal_quarter=request.fiscal_quarter,
            filing_date=None,
            content=content,
        )

    def _resolve_document_type(
        self,
        plan: AnalysisPlan,
    ) -> DocumentType:

        if DocumentType.TEN_K in plan.required_documents:
            return DocumentType.TEN_K

        if DocumentType.TEN_Q in plan.required_documents:
            return DocumentType.TEN_Q

        raise ValueError(
            "AnalysisPlan does not request an SEC filing."
        )

    def _get_test_filing_url(
        self,
        document_type: DocumentType,
    ) -> str:

        if document_type is DocumentType.TEN_K:
            return (
                "https://www.sec.gov/Archives/edgar/data/"
                "320193/"
                "000032019324000123/"
                "aapl-20240928.htm"
            )

        raise NotImplementedError(
            "Test URL for 10-Q has not been configured."
        )