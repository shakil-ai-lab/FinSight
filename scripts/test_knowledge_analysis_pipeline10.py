from __future__ import annotations

from pathlib import Path

from app.core import configure_logging

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
    ResponseParser as ExtractionResponseParser,
)

from app.infrastructure.llm.knowledge_analysis import (
    AnalysisMapper,
    AnalysisPrompt,
    GeminiKnowledgeAnalyzer,
    ResponseParser as AnalysisResponseParser,
)

from app.application.services import KnowledgeAnalysisService


def load_test_document() -> ParsedDocument:
    """
    Load and parse the sample SEC filing.
    """

    html_path = Path("data/raw/sec/apple_10k.html")

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

    return GeminiKnowledgeExtractor(
        client=GeminiClient(),
        prompt=KnowledgeExtractionPrompt(),
        response_parser=ExtractionResponseParser(),
        mapper=ExtractedKnowledgeMapper(),
    )


def build_analyzer() -> KnowledgeAnalysisService:

    analyzer = GeminiKnowledgeAnalyzer(
        client=GeminiClient(),
        prompt=AnalysisPrompt(),
        response_parser=AnalysisResponseParser(),
        mapper=AnalysisMapper(),
    )

    return KnowledgeAnalysisService(analyzer)


def validate_results(insights):

    assert insights is not None

    # MVP supports single-document analysis only.
    assert insights.quarter_comparison is None
    assert insights.trend_analysis is None

    # These analyses must always be produced.
    assert insights.consistency_analysis is not None
    assert insights.communication_analysis is not None


def print_results(insights):

    print("\n" + "=" * 80)
    print("QUARTER COMPARISON")
    print("=" * 80)

    if insights.quarter_comparison:
        print(insights.quarter_comparison)
    else:
        print("Not available (requires historical filings).")


    print("\n" + "=" * 80)
    print("TREND ANALYSIS")
    print("=" * 80)

    if insights.trend_analysis:
        print(insights.trend_analysis)
    else:
        print("Not available (requires historical filings).")


def main():

    configure_logging()

    print("=" * 80)
    print("Knowledge Analysis Integration Test")
    print("=" * 80)

    print("\nLoading document...")

    document = load_test_document()

    print("✓ Document loaded")

    extractor = build_extractor()

    analysis_service = build_analyzer()

    print("\nRunning knowledge extraction...")

    knowledge = extractor.extract(document)

    print("✓ Knowledge extraction completed")

    print("\nRunning knowledge analysis...")

    insights = analysis_service.analyze(knowledge)

    print("✓ Knowledge analysis completed")

    validate_results(insights)

    print_results(insights)

    print("\n" + "=" * 80)
    print("Integration Test Passed Successfully")
    print("=" * 80)

if __name__ == "__main__": 
    main()    