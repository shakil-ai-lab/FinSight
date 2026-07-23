from __future__ import annotations

from pathlib import Path

from app.domain.documents import (
    DocumentSource,
    DocumentType,
    SourceDocument,
)

from app.infrastructure.parsing import SECDocumentParser

from app.application.models import ParsedDocument

from app.infrastructure.llm.gemini import GeminiClient

from app.infrastructure.llm.knowledge_extraction import (
    ExtractedKnowledgeMapper,
    GeminiKnowledgeExtractor,
    KnowledgeExtractionPrompt,
    ResponseParser,
)


def load_test_document() -> ParsedDocument:
    """
    Load and parse the sample SEC filing used for integration testing.
    """

    html_path = Path("data/raw/sec/apple_10k.html")

    if not html_path.exists():
        raise FileNotFoundError(
            f"Test document not found: {html_path}"
        )

    html = html_path.read_text(
        encoding="utf-8",
        errors="ignore",
    )

    source_document = SourceDocument(
        company="Apple",
        document_type=DocumentType.TEN_K,
        source=DocumentSource.EDGAR,
        fiscal_year=2024,
        fiscal_quarter=None,
        filing_date=None,
        content=html,
    )

    parser = SECDocumentParser()

    return parser.parse(source_document)


def build_extractor() -> GeminiKnowledgeExtractor:
    """
    Construct the complete extraction pipeline.
    """

    return GeminiKnowledgeExtractor(
        client=GeminiClient(),
        prompt=KnowledgeExtractionPrompt(),
        response_parser=ResponseParser(),
        mapper=ExtractedKnowledgeMapper(),
    )


def print_results(knowledge) -> None:
    """
    Pretty-print extracted knowledge.
    """

    print("\n" + "=" * 80)
    print("FINANCIAL SNAPSHOT")
    print("=" * 80)
    print(knowledge.financial_snapshot)

    print("\n" + "=" * 80)
    print("BUSINESS SEGMENTS")
    print("=" * 80)
    print(knowledge.business_segments)

    print("\n" + "=" * 80)
    print("MANAGEMENT DISCUSSION")
    print("=" * 80)
    print(knowledge.management_discussion)

    print("\n" + "=" * 80)
    print("RISK ASSESSMENT")
    print("=" * 80)
    print(knowledge.risk_assessment)

    print("\n" + "=" * 80)
    print("GUIDANCE SUMMARY")
    print("=" * 80)
    print(knowledge.guidance_summary)

    print("\n" + "=" * 80)
    print("TRANSCRIPT ANALYSIS")
    print("=" * 80)
    print(knowledge.transcript_analysis)


def validate_results(knowledge) -> None:
    """
    Basic integration assertions.
    """

    assert knowledge is not None

    assert knowledge.financial_snapshot is not None

    assert knowledge.business_segments is not None

    assert knowledge.management_discussion is not None

    assert knowledge.risk_assessment is not None

    assert knowledge.guidance_summary is not None

    assert knowledge.transcript_analysis is not None


def main() -> None:

    print("=" * 80)
    print("Gemini Knowledge Extraction Integration Test")
    print("=" * 80)

    print("\nLoading test document...")

    document = load_test_document()

    print("✓ Document loaded")

    print(
        f"Characters: {len(document.text):,}"
    )

    extractor = build_extractor()

    print("\nRunning extraction pipeline...")

    knowledge = extractor.extract(
        document
    )

    print("✓ Extraction completed")

    validate_results(
        knowledge
    )

    print_results(
        knowledge
    )

    print("\n" + "=" * 80)
    print("Integration Test Passed Successfully")
    print("=" * 80)


if __name__ == "__main__":
    main()