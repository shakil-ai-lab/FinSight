from __future__ import annotations

from bs4 import BeautifulSoup

from app.application.models import ParsedDocument
from app.application.ports import DocumentParser
from app.domain.documents import SourceDocument


class SECDocumentParser(DocumentParser):
    """
    Infrastructure implementation of the DocumentParser port.

    Responsible for converting raw SEC filing HTML into
    clean readable text suitable for downstream knowledge extraction.
    """

    def parse(self, document: SourceDocument) -> str:
        """
        Parse an SEC filing into plain text.

        Parameters
        ----------
        document:
            Raw SEC filing.

        Returns
        -------
        str
            Clean text extracted from the filing.
        """

        soup = BeautifulSoup(document.content, "html.parser")

        # Remove scripts and styling
        for tag in soup(["script", "style"]):
            tag.decompose()

        text = soup.get_text(separator="\n")

        # Remove blank lines
        lines = (
            line.strip()
            for line in text.splitlines()
        )

        cleaned = "\n".join(
            line
            for line in lines
            if line
        )

        return ParsedDocument(
    document_type=document.document_type.value,
    text=cleaned,
)