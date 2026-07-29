from __future__ import annotations

from decimal import Decimal
from typing import Optional

from app.application.models import PresentationOutput

from app.interfaces.streamlit.view_models.dashboard_view import (
    BusinessSegmentView,
    DashboardView,
)


def _format_billions(value: Optional[Decimal]) -> str:
    """
    Format a Decimal monetary value into billions.
    """

    if value is None:
        return "N/A"

    return f"${float(value) / 1_000_000_000:.1f}B"


def _format_eps(value: Optional[Decimal]) -> str:
    """
    Format earnings per share.
    """

    if value is None:
        return "N/A"

    return f"${float(value):.2f}"


def _format_growth(value: Optional[Decimal]) -> str:
    """
    Format percentage growth.
    """

    if value is None:
        return "N/A"

    return f"{float(value):+.2f}%"


def map_dashboard(
    presentation: PresentationOutput,
) -> DashboardView:
    """
    Convert the PresentationOutput into a DashboardView.

    This is the only place where the Streamlit layer
    understands the application object graph.
    """

    brief = presentation.analyst_brief
    knowledge = presentation.extracted_knowledge

    materiality = brief.materiality_assessment

    consistency = materiality.consistency_analysis
    communication = materiality.communication_analysis

    snapshot = knowledge.financial_snapshot
    business_segments = knowledge.business_segments
    risks = knowledge.risk_assessment

    return DashboardView(

        # --------------------------------------------------
        # Recommendation Card
        # --------------------------------------------------

        recommendation=(
            materiality.recommendation
            or brief.recommendation
        ),

        overall_assessment=(
            materiality.overall_assessment
            or brief.executive_summary
        ),

        confidence=(
            f"{consistency.consistency_score}%"
            if consistency.consistency_score is not None
            else "N/A"
        ),

        # --------------------------------------------------
        # Executive Summary
        # --------------------------------------------------

        executive_summary=brief.executive_summary,

        # --------------------------------------------------
        # Financial Snapshot
        # --------------------------------------------------

        revenue=_format_billions(
            snapshot.revenue
        ),

        operating_cash_flow=_format_billions(
            snapshot.operating_cash_flow
        ),

        net_income=_format_billions(
            snapshot.net_income
        ),

        earnings_per_share=_format_eps(
            snapshot.earnings_per_share
        ),

        # --------------------------------------------------
        # Business Segments
        # --------------------------------------------------

        business_segments=[

            BusinessSegmentView(
                name=segment.name,

                revenue=_format_billions(
                    segment.revenue
                ),

                growth=_format_growth(
                    segment.growth_rate
                ),
            )

            for segment in business_segments.segments

        ],

        # --------------------------------------------------
        # Risk Assessment
        # --------------------------------------------------

        risk_assessment=[

            f"{risk.title}: {risk.description}"

            for risk in risks.risks

        ],

        # --------------------------------------------------
        # Consistency Analysis
        # --------------------------------------------------

        consistency_analysis=(

            ([consistency.summary]
             if consistency.summary
             else [])

            + list(
                consistency.supporting_observations
            )

            + list(
                consistency.inconsistencies
            )

        ),

        # --------------------------------------------------
        # Communication Analysis
        # --------------------------------------------------

        communication_analysis=(

            ([communication.summary]
             if communication.summary
             else [])

            + list(
                communication.key_messages
            )

            + list(
                communication.notable_concerns
            )

        ),

        # --------------------------------------------------
        # Decision Support
        # --------------------------------------------------

        investment_highlights=list(
            brief.investment_highlights
        ),

        key_risks=list(
            brief.key_risks
        ),
    )