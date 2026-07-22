from __future__ import annotations

from decimal import Decimal

from app.infrastructure.llm.knowledge_extraction.extracted_knowledge_mapper import (
    ExtractedKnowledgeMapper,
)


def test_financial_snapshot(
    mapper: ExtractedKnowledgeMapper,
) -> None:

    print("\nTesting FinancialSnapshot...")

    data = {
        "company": "Apple Inc.",
        "fiscal_year": 2025,
        "fiscal_quarter": 2,
        "revenue": "94036000000",
        "gross_margin": "0.462",
        "operating_income": "29591000000",
        "net_income": "24778000000",
        "earnings_per_share": "1.65",
        "operating_cash_flow": "28765000000",
    }

    snapshot = mapper._map_financial_snapshot(data)

    assert snapshot.company == "Apple Inc."
    assert snapshot.fiscal_year == 2025
    assert snapshot.fiscal_quarter == 2

    assert snapshot.revenue == Decimal("94036000000")
    assert snapshot.gross_margin == Decimal("0.462")
    assert snapshot.operating_income == Decimal("29591000000")
    assert snapshot.net_income == Decimal("24778000000")
    assert snapshot.earnings_per_share == Decimal("1.65")
    assert snapshot.operating_cash_flow == Decimal("28765000000")

    print("✓ FinancialSnapshot mapping passed.")


def test_business_segments(
    mapper: ExtractedKnowledgeMapper,
) -> None:

    print("\nTesting BusinessSegments...")

    data = {
        "company": "Apple Inc.",
        "fiscal_year": 2025,
        "fiscal_quarter": 2,
        "segments": [
            {
                "name": "iPhone",
                "revenue": "201000000000",
                "operating_income": "85000000000",
                "growth_rate": "5.2",
                "description": "iPhone business",
            },
            {
                "name": "Services",
                "revenue": "96000000000",
                "operating_income": "42000000000",
                "growth_rate": "12.8",
                "description": "Services business",
            },
        ],
    }

    business_segments = mapper._map_business_segments(data)

    assert business_segments.company == "Apple Inc."
    assert business_segments.fiscal_year == 2025
    assert business_segments.fiscal_quarter == 2

    assert len(business_segments.segments) == 2

    iphone = business_segments.segments[0]

    assert iphone.name == "iPhone"
    assert iphone.revenue == Decimal("201000000000")
    assert iphone.operating_income == Decimal("85000000000")
    assert iphone.growth_rate == Decimal("5.2")
    assert iphone.description == "iPhone business"

    services = business_segments.segments[1]

    assert services.name == "Services"
    assert services.revenue == Decimal("96000000000")
    assert services.operating_income == Decimal("42000000000")
    assert services.growth_rate == Decimal("12.8")
    assert services.description == "Services business"

    print("✓ BusinessSegments mapping passed.")

# management discusssion test
def test_management_discussion(
    mapper: ExtractedKnowledgeMapper,
) -> None:

    print("\nTesting ManagementDiscussion...")

    data = {
        "company": "Apple Inc.",
        "fiscal_year": 2025,
        "fiscal_quarter": 2,
        "business_summary": (
            "Apple delivered record services revenue."
        ),
        "performance_drivers": [
            "Strong iPhone demand",
            "Growth in Services",
        ],
        "operational_highlights": [
            "Expanded AI features",
            "Supply chain improvements",
        ],
        "strategic_initiatives": [
            "AI investment",
            "Global expansion",
        ],
        "management_commentary": [
            "Management remains optimistic.",
        ],
    }

    discussion = mapper._map_management_discussion(data)

    assert discussion.company == "Apple Inc."
    assert discussion.fiscal_year == 2025
    assert discussion.fiscal_quarter == 2

    assert discussion.business_summary == (
        "Apple delivered record services revenue."
    )

    assert discussion.performance_drivers == (
        "Strong iPhone demand",
        "Growth in Services",
    )

    assert discussion.operational_highlights == (
        "Expanded AI features",
        "Supply chain improvements",
    )

    assert discussion.strategic_initiatives == (
        "AI investment",
        "Global expansion",
    )

    assert discussion.management_commentary == (
        "Management remains optimistic.",
    )

    print("✓ ManagementDiscussion mapping passed.")


def main() -> None:

    print("=" * 70)
    print("ExtractedKnowledgeMapper Tests")
    print("=" * 70)

    mapper = ExtractedKnowledgeMapper()

    test_financial_snapshot(mapper)

    test_business_segments(mapper)

    test_management_discussion(mapper)

    print("\n" + "=" * 70)
    print("All mapper tests passed successfully.")
    print("=" * 70)


if __name__ == "__main__":
    main()