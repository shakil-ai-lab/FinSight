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

from app.application.services import DecisionSupportService

from app.infrastructure.llm.decision_support import (
    DecisionSupportMapper,
    DecisionSupportPrompt,
    GeminiDecisionSupportEngine,
    ResponseParser as DecisionResponseParser,
)

from app.application.services import KnowledgeAnalysisService

from app.application.services import PresentationService

from app.infrastructure.llm.presentation.simple_presentation_engine import SimplePresentationEngine


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

def build_decision_support() -> DecisionSupportService:

    engine = GeminiDecisionSupportEngine(
        client=GeminiClient(),
        prompt_builder=DecisionSupportPrompt(),
        response_parser=DecisionResponseParser(),
        mapper=DecisionSupportMapper(),
    )

    return DecisionSupportService(engine)

def build_presentation() -> PresentationService:

    engine = SimplePresentationEngine()

    return PresentationService(engine)


def validate_results(result, brief):

    assert result is not None
    assert brief is not None

    assert result.materiality_assessment is not None

    assert (
        result.materiality_assessment.overall_assessment
        is not None
    )

    assert brief.executive_summary != ""

    assert brief.recommendation != ""

def print_results(result, brief):

    # brief = result.analyst_brief

    assessment = result.materiality_assessment

    # assessment = result.materiality_assessment

    print("\n" + "=" * 80)
    print("EXECUTIVE SUMMARY")
    print("=" * 80)
    print(brief.executive_summary)

    print("\n" + "=" * 80)
    print("RECOMMENDATION")
    print("=" * 80)
    print(brief.recommendation)

    print("\n" + "=" * 80)
    print("OVERALL ASSESSMENT")
    print("=" * 80)
    print(assessment.overall_assessment)

    print("\n" + "=" * 80)
    print("CRITICAL FINDINGS")
    print("=" * 80)

    for item in assessment.critical_findings:
        print("-", item)


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

    decision_service = build_decision_support()

    presentation_service = build_presentation()

    print("\nRunning knowledge extraction...")

    knowledge = extractor.extract(document)

    print("✓ Knowledge extraction completed")

    print("\nRunning knowledge analysis...")

    insights = analysis_service.analyze(knowledge)

    print("✓ Knowledge analysis completed")

    print("\nRunning decision support...")

    result = decision_service.generate_decision_support(
        knowledge,
        insights,
    )

    print("✓ Decision support completed")

    print("\nRunning presentation...")

    brief = presentation_service.present(result)

    print("✓ Presentation completed")

    validate_results(result, brief)

    print_results(result, brief)

    print("\n" + "=" * 80)
    print("Integration Test Passed Successfully")
    print("=" * 80)

if __name__ == "__main__": 
    main()    