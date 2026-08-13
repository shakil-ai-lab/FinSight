from __future__ import annotations

import streamlit as st

from app.interfaces.streamlit.mappers.dashboard_mapper import (
    map_dashboard,
)

from app.bootstrap import (
    build_analysis_orchestrator,
    build_filing_discovery_service,
)

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
    # orchestrator = build_analysis_orchestrator()

    # ------------------------------------------------------------
    # Header
    # ------------------------------------------------------------

    render_header()

    # ------------------------------------------------------------
    # Sidebar
    # ------------------------------------------------------------

    filing_discovery_service = build_filing_discovery_service()

    sidebar = render_sidebar(
        filing_discovery_service=filing_discovery_service,
    )

    if "brief" not in st.session_state:
        st.session_state.brief = None

    if sidebar.analyze_clicked and sidebar.analysis_request is not None:
        orchestrator = build_analysis_orchestrator()
        st.session_state.brief = orchestrator.analyze(
            sidebar.analysis_request
        )

    brief = st.session_state.brief

    if brief is None:
        st.info("Select a company, Filing Type, Fiscal Year and click 'Analyze Company' to begin.")
        return

    view = map_dashboard(brief)
    # ------------------------------------------------------------
    # Demo Data
    # ------------------------------------------------------------

    # ------------------------------------------------------------
    # Recommendation
    # ------------------------------------------------------------

    render_recommendation_card(
        recommendation=view.recommendation,
        overall_assessment=view.overall_assessment,
        confidence=view.confidence,
    )

    # ------------------------------------------------------------
    # Executive Summary
    # ------------------------------------------------------------

    render_executive_summary(
        view.executive_summary,
    )

    # ------------------------------------------------------------
    # Financial Snapshot
    # ------------------------------------------------------------

    render_financial_snapshot(
        revenue=view.revenue,
        operating_cash_flow=view.operating_cash_flow,
        net_income=view.net_income,
        diluted_eps=view.earnings_per_share,
    )

    # ------------------------------------------------------------
    # Business Segments
    # ------------------------------------------------------------

    render_business_segments(
        view.business_segments,
    )

    # ------------------------------------------------------------
    # Analysis Tabs
    # ------------------------------------------------------------

    render_analysis_tabs(
        risk_assessment=view.risk_assessment,
        consistency_analysis=view.consistency_analysis,
        communication_analysis=view.communication_analysis,
        investment_highlights=view.investment_highlights,
        key_risks=view.key_risks,
    )

