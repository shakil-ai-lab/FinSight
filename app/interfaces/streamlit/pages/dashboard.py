from __future__ import annotations

from app.interfaces.streamlit.components.analysis_tabs import (
    render_analysis_tabs,
)
from app.interfaces.streamlit.components.business_segments import (
    BusinessSegmentView,
    render_business_segments,
)
from app.interfaces.streamlit.components.executive_summary import (
    render_executive_summary,
)
from app.interfaces.streamlit.components.financial_snapshot import (
    render_financial_snapshot,
)
from app.interfaces.streamlit.components.header import (
    render_header,
)
from app.interfaces.streamlit.components.recommendation_card import (
    render_recommendation_card,
)
from app.interfaces.streamlit.components.sidebar import (
    render_sidebar,
)


def render_dashboard() -> None:
    """
    Render the FinSight dashboard.

    Currently uses demonstration data.
    Later this page will call AnalysisOrchestrator.
    """

    # ------------------------------------------------------------
    # Header
    # ------------------------------------------------------------

    render_header()

    # ------------------------------------------------------------
    # Sidebar
    # ------------------------------------------------------------

    sidebar = render_sidebar()

    # ------------------------------------------------------------
    # Demo Data
    # ------------------------------------------------------------

    recommendation = "Buy"

    executive_summary = (
        "Apple Inc. remains a premier cash-generating powerhouse "
        "with strong operating cash flow, excellent capital returns, "
        "and continued Services growth. Investors should monitor "
        "regulatory developments and the slowdown in Greater China."
    )

    # ------------------------------------------------------------
    # Recommendation
    # ------------------------------------------------------------

    render_recommendation_card(
        recommendation=recommendation,
        overall_assessment=executive_summary,
        confidence="High",
    )

    # ------------------------------------------------------------
    # Executive Summary
    # ------------------------------------------------------------

    render_executive_summary(
        executive_summary,
    )

    # ------------------------------------------------------------
    # Financial Snapshot
    # ------------------------------------------------------------

    render_financial_snapshot(
        revenue="$391.04B",
        operating_cash_flow="$118.25B",
        net_income="$93.74B",
        diluted_eps="$6.08",
    )

    # ------------------------------------------------------------
    # Business Segments
    # ------------------------------------------------------------

    render_business_segments(
        [
            BusinessSegmentView(
                "Americas",
                "$167.0B",
                "+2.76%",
            ),
            BusinessSegmentView(
                "Europe",
                "$101.3B",
                "+7.46%",
            ),
            BusinessSegmentView(
                "Greater China",
                "$66.9B",
                "-7.73%",
            ),
            BusinessSegmentView(
                "Japan",
                "$25.0B",
                "+5.12%",
            ),
            BusinessSegmentView(
                "Rest of Asia Pacific",
                "$30.7B",
                "+8.10%",
            ),
        ]
    )

    # ------------------------------------------------------------
    # Analysis Tabs
    # ------------------------------------------------------------

    render_analysis_tabs(
        risk_assessment=[
            "Regulatory pressure continues to increase globally.",
            "Manufacturing concentration remains high in Asia.",
            "Greater China revenue continues to decline.",
        ],
        consistency_analysis=[
            "Financial performance remains highly consistent.",
            "Strong operating cash flow continues to support dividends.",
        ],
        communication_analysis=[
            "Management tone remains optimistic.",
            "Future AI initiatives received significant emphasis.",
        ],
        investment_highlights=[
            "$110.2B returned to shareholders.",
            "Services continues double-digit profitability.",
            "Operating Cash Flow reached $118.25B.",
        ],
        key_risks=[
            "Greater China slowdown.",
            "European antitrust investigations.",
            "Supply chain concentration.",
        ],
    )

    # ------------------------------------------------------------
    # Future
    # ------------------------------------------------------------

    if sidebar.analyze_clicked:
        pass