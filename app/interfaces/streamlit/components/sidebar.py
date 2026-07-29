from __future__ import annotations

from dataclasses import dataclass

import streamlit as st


@dataclass(slots=True, frozen=True)
class SidebarState:
    """
    User selections from the Streamlit sidebar.
    """

    company_ticker: str
    filing_type: str
    analyze_clicked: bool


def render_sidebar() -> SidebarState:
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

        st.divider()

        analyze_clicked = st.button(
            "Analyze Company",
            type="primary",
            use_container_width=True,
        )

    return SidebarState(
        company_ticker=company_ticker,
        filing_type=filing_type,
        analyze_clicked=analyze_clicked,
    )