from __future__ import annotations

from app.application.exceptions import (
    KnowledgeExtractionError,
    LLMGenerationError,
)

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
    ResponseParser,
)

# TEST_CASE = "mapper_failure"    >>> not tested
# TEST_CASE = "invalid_severity"  >>> not tested

# TEST_CASE = None
# TEST_CASE = "invalid_json"
# TEST_CASE = "empty_response"

# TEST_CASE = "malformed_json_structure"
# Options:
# None
# invalid_json
# empty_response
# mapper_failure
# invalid_severity
# server_error
# TEST_CASE = "server_error"
# unexpected_exception
TEST_CASE = "unexpected_exception"

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


def apply_failure(extractor: GeminiKnowledgeExtractor) -> None:
    """
    Inject failures into the extraction pipeline without
    modifying production code.
    """

    if TEST_CASE == "invalid_json":

        extractor._client.generate = (
            lambda prompt: "{ invalid json"
        )

    elif TEST_CASE == "empty_response":

        class FakeResponse:
            text = ""

        extractor._client._client.models.generate_content = (
            lambda **kwargs: FakeResponse()
        )

    elif TEST_CASE == "mapper_failure":

        def fake_map(data):
            raise ValueError(
                "Simulated mapper failure."
            )

        extractor._mapper.map = fake_map

    elif TEST_CASE == "invalid_severity":

        def fake_generate(prompt):
            return """
            {
              "financial_snapshot": {},
              "business_segments": [],
              "management_discussion": {},
              "risk_assessment": {
                "overall_severity": "VERY_HIGH_PLUS",
                "risks": []
              },
              "guidance_summary": {},
              "transcript_analysis": {}
            }
            """

        extractor._client.generate = fake_generate

    elif TEST_CASE == "server_error":

        def fake_generate(prompt):
            raise LLMGenerationError(
                "Simulated Gemini server failure."
            )

        extractor._client.generate = fake_generate

    elif TEST_CASE == "unexpected_exception":

        def fake_build(document):
            raise RuntimeError(
                "Unexpected prompt generation bug."
            )

        extractor._prompt.build = fake_build

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

    configure_logging()

    print("=" * 80)
    # print("Gemini Knowledge Extraction Integration Test")
    if TEST_CASE is None:
        print("Gemini Knowledge Extraction Integration Test")
    else:
        print(f"Knowledge Extraction Failure Test ({TEST_CASE})")
    print("=" * 80)

    print("\nLoading test document...")

    document = load_test_document()

    print("✓ Document loaded")

    print(
        f"Characters: {len(document.text):,}"
    )

    extractor = build_extractor()

    apply_failure(extractor)

    print("\nRunning extraction pipeline...")

    try:

        knowledge = extractor.extract(document)

        if TEST_CASE is not None:
            print("\n❌ Expected an exception, but extraction succeeded.")
            return

        print("✓ Extraction completed")

        validate_results(knowledge)

        print_results(knowledge)

    except KnowledgeExtractionError as exc:

        print("\n" + "=" * 80)
        print("EXPECTED APPLICATION EXCEPTION")
        print("=" * 80)

        print(f"Type    : {type(exc).__name__}")
        print(f"Message : {exc}")

        print("\n✓ Correct application exception raised.")

    except Exception as exc:

        print("\n" + "=" * 80)
        print("UNEXPECTED EXCEPTION")
        print("=" * 80)

        print(f"Type    : {type(exc).__name__}")
        print(f"Message : {exc}")

        print("\n❌ Unexpected programming exception.")
    print("\n" + "=" * 80)

    if TEST_CASE is None:
        print("Integration Test Passed Successfully")
    else:
        print("Failure Test Completed")

    print("=" * 80)

if __name__ == "__main__":
    main()