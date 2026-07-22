from __future__ import annotations

from decimal import Decimal

from app.infrastructure.llm.knowledge_extraction.extracted_knowledge_mapper import (
    ExtractedKnowledgeMapper,
)


def main() -> None:
    print("=" * 60)
    print("ExtractedKnowledgeMapper Test")
    print("=" * 60)

    mapper = ExtractedKnowledgeMapper()

    snapshot_data = {
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

    print("\nMapping FinancialSnapshot...")

    financial_snapshot = mapper._map_financial_snapshot(snapshot_data)

    print("✓ FinancialSnapshot created successfully.\n")

    print(financial_snapshot)

    print("\nRunning Assertions...")

    assert financial_snapshot.company == "Apple Inc."
    assert financial_snapshot.fiscal_year == 2025
    assert financial_snapshot.fiscal_quarter == 2

    assert financial_snapshot.revenue == Decimal("94036000000")
    assert financial_snapshot.gross_margin == Decimal("0.462")
    assert financial_snapshot.operating_income == Decimal("29591000000")
    assert financial_snapshot.net_income == Decimal("24778000000")
    assert financial_snapshot.earnings_per_share == Decimal("1.65")
    assert financial_snapshot.operating_cash_flow == Decimal("28765000000")

    print("✓ Company OK")
    print("✓ Fiscal Year OK")
    print("✓ Fiscal Quarter OK")
    print("✓ Revenue OK")
    print("✓ Gross Margin OK")
    print("✓ Operating Income OK")
    print("✓ Net Income OK")
    print("✓ EPS OK")
    print("✓ Operating Cash Flow OK")

    print("\n" + "=" * 60)
    print("All mapper tests passed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()