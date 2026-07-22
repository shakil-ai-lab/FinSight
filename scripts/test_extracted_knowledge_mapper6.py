from __future__ import annotations

from decimal import Decimal

from app.domain.knowledge import RiskSeverity

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

# Risk Assessment
def test_risk_assessment(
    mapper: ExtractedKnowledgeMapper,
) -> None:

    print("\nTesting RiskAssessment...")

    data = {
        "company": "Apple Inc.",
        "fiscal_year": 2025,
        "fiscal_quarter": 2,
        "overall_summary": (
            "Apple faces moderate operational risks."
        ),
        "risks": [
            {
                "title": "Supply Chain",
                "category": "Operations",
                "description": "Supplier disruptions.",
                "severity": "High",
                "evidence": "10-K Risk Factors",
            },
            {
                "title": "Regulatory",
                "category": "Legal",
                "description": "Antitrust investigations.",
                "severity": "Medium",
                "evidence": "Regulatory filings",
            },
        ],
    }

    assessment = mapper._map_risk_assessment(data)

    assert assessment.company == "Apple Inc."
    assert assessment.fiscal_year == 2025
    assert assessment.fiscal_quarter == 2

    assert assessment.overall_summary == (
        "Apple faces moderate operational risks."
    )

    assert len(assessment.risks) == 2

    risk = assessment.risks[0]

    assert risk.title == "Supply Chain"
    assert risk.category == "Operations"
    assert risk.description == "Supplier disruptions."
    assert risk.severity == RiskSeverity.HIGH
    assert risk.evidence == "10-K Risk Factors"

    print("✓ RiskAssessment mapping passed.")    

# guidance summary test
def test_guidance_summary(
    mapper: ExtractedKnowledgeMapper,
) -> None:

    print("\nTesting GuidanceSummary...")

    data = {
        "company": "Apple Inc.",
        "fiscal_year": 2025,
        "fiscal_quarter": 2,
        "revenue_guidance": "High single-digit growth",
        "earnings_guidance": "EPS expected to improve",
        "margin_guidance": "Gross margin 46-47%",
        "cash_flow_guidance": "Strong operating cash flow",
        "capital_expenditure_guidance": "$12B planned",
        "strategic_outlook": [
            "Expand AI capabilities",
            "Increase Services revenue",
        ],
        "management_expectations": [
            "Continued long-term growth",
            "Innovation remains priority",
        ],
    }

    guidance = mapper._map_guidance_summary(data)

    assert guidance.company == "Apple Inc."
    assert guidance.fiscal_year == 2025
    assert guidance.fiscal_quarter == 2

    assert (
        guidance.revenue_guidance
        == "High single-digit growth"
    )

    assert (
        guidance.earnings_guidance
        == "EPS expected to improve"
    )

    assert (
        guidance.margin_guidance
        == "Gross margin 46-47%"
    )

    assert (
        guidance.cash_flow_guidance
        == "Strong operating cash flow"
    )

    assert (
        guidance.capital_expenditure_guidance
        == "$12B planned"
    )

    assert guidance.strategic_outlook == (
        "Expand AI capabilities",
        "Increase Services revenue",
    )

    assert guidance.management_expectations == (
        "Continued long-term growth",
        "Innovation remains priority",
    )

    print("✓ GuidanceSummary mapping passed.")


def main() -> None:

    print("=" * 70)
    print("ExtractedKnowledgeMapper Tests")
    print("=" * 70)

    mapper = ExtractedKnowledgeMapper()

    test_financial_snapshot(mapper)

    test_business_segments(mapper)

    test_management_discussion(mapper)

    test_risk_assessment(mapper)

    test_guidance_summary(mapper)

    print("\n" + "=" * 70)
    print("All mapper tests passed successfully.")
    print("=" * 70)


if __name__ == "__main__":
    main()