from __future__ import annotations

from dataclasses import dataclass

from datetime import datetime

from app.domain.fiscal import FiscalQuarter

import streamlit as st

from app.domain.analysis import AnalysisRequest, AnalysisType


@dataclass(slots=True, frozen=True)
class SidebarResult:
    """
    Result returned by the Streamlit sidebar.
    """

    analysis_request: AnalysisRequest
    analyze_clicked: bool


def render_sidebar() -> SidebarResult:
    """
    Render the application sidebar and return the user's selections.
    """

    with st.sidebar:
        st.header("Analysis")

        company_ticker = st.text_input(
            "Company Ticker",
            value="AAPL",
            help="Enter a valid SEC ticker symbol.",
        ).upper()

        filing_type = st.selectbox(
            "Filing Type",
            options=["10-K", "10-Q"],
            index=0,
        )
        current_year = datetime.now().year

        fiscal_year = st.number_input(
            "Fiscal Year",
            min_value=2000,
            max_value=current_year,
            value=current_year - 1,
            step=1,
        )

        fiscal_quarter = None

        if filing_type == "10-Q":
            fiscal_quarter = st.selectbox(
                "Fiscal Quarter",
                options=list(FiscalQuarter),
                index=0,
                format_func=str,
            )

        st.divider()

        analyze_clicked = st.button(
            "Analyze Company",
            type="primary",
            use_container_width=True,
        )

    analysis_request = AnalysisRequest(
        company=company_ticker,
        ticker=company_ticker,
        analysis_type=(
            AnalysisType.ANNUAL
            if filing_type == "10-K"
            else AnalysisType.QUARTERLY
        ),
        fiscal_year=int(fiscal_year),
        fiscal_quarter=fiscal_quarter,
)

    return SidebarResult(
        analysis_request=analysis_request,
        analyze_clicked=analyze_clicked,
    )