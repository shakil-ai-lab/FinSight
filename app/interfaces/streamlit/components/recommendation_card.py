from __future__ import annotations

import streamlit as st


_STATUS = {
    "BUY": ("🟢", "success"),
    "HOLD": ("🟡", "warning"),
    "SELL": ("🔴", "error"),
}


def render_recommendation_card(
    recommendation: str,
    overall_assessment: str,
    confidence: str | None = None,
) -> None:
    """
    Render the investment recommendation card.

    Parameters
    ----------
    recommendation:
        Buy / Hold / Sell

    overall_assessment:
        AI-generated investment assessment.

    confidence:
        Optional confidence level.
    """

    recommendation = recommendation.upper()

    icon, status = _STATUS.get(
        recommendation,
        ("🔵", "info"),
    )

    with st.container(border=True):

        col1, col2 = st.columns([3, 1])

        with col1:
            st.subheader(f"{icon} {recommendation}")

        with col2:
            if confidence:
                st.metric(
                    "Confidence",
                    confidence,
                )

        getattr(st, status)(
            overall_assessment,
            icon="📈",
        )