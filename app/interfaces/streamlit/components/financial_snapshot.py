from __future__ import annotations

import streamlit as st


def render_financial_snapshot(
    revenue: str,
    operating_cash_flow: str,
    net_income: str,
    diluted_eps: str,
) -> None:
    """
    Render the company's key financial metrics.
    """

    with st.container(border=True):

        st.subheader("💰 Financial Snapshot")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                label="Revenue",
                value=revenue,
            )

            st.metric(
                label="Net Income",
                value=net_income,
            )

        with col2:
            st.metric(
                label="Operating Cash Flow",
                value=operating_cash_flow,
            )

            st.metric(
                label="Diluted EPS",
                value=diluted_eps,
            )