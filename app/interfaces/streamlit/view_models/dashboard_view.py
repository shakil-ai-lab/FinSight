from __future__ import annotations

from dataclasses import dataclass



@dataclass(slots=True, frozen=True)
class BusinessSegmentView:
    """
    UI representation of a business segment.
    """

    name: str
    revenue: str
    growth: str


@dataclass(slots=True, frozen=True)
class DashboardView:
    """
    Presentation model consumed by the Streamlit dashboard.

    All values are already formatted and ready for display.
    No domain objects should appear in this model.
    """

    # Recommendation Card
    recommendation: str
    overall_assessment: str
    confidence: str

    # Executive Summary
    executive_summary: str

    # Financial Snapshot
    revenue: str
    operating_cash_flow: str
    net_income: str
    earnings_per_share: str

    # Business Segments
    business_segments: list[BusinessSegmentView]

    # Analysis Tabs
    risk_assessment: list[str]
    consistency_analysis: list[str]
    communication_analysis: list[str]
    investment_highlights: list[str]
    key_risks: list[str]