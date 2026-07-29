from __future__ import annotations

import streamlit as st


def render_analysis_tabs(
    risk_assessment: list[str],
    consistency_analysis: list[str],
    communication_analysis: list[str],
    investment_highlights: list[str],
    key_risks: list[str],
) -> None:
    """
    Render detailed AI analysis in tabbed sections.
    """

    (
        risk_tab,
        consistency_tab,
        communication_tab,
        highlights_tab,
        key_risks_tab,
    ) = st.tabs(
        [
            "📉 Risk Assessment",
            "📊 Consistency",
            "🗣 Communication",
            "⭐ Highlights",
            "⚠ Key Risks",
        ]
    )

    with risk_tab:
        _render_list(
            title="Risk Assessment",
            items=risk_assessment,
            empty_message="No risk assessment available.",
        )

    with consistency_tab:
        _render_list(
            title="Consistency Analysis",
            items=consistency_analysis,
            empty_message="No consistency analysis available.",
        )

    with communication_tab:
        _render_list(
            title="Communication Analysis",
            items=communication_analysis,
            empty_message="No communication analysis available.",
        )

    with highlights_tab:
        _render_list(
            title="Investment Highlights",
            items=investment_highlights,
            empty_message="No investment highlights available.",
        )

    with key_risks_tab:
        _render_list(
            title="Key Risks",
            items=key_risks,
            empty_message="No key risks available.",
        )


def _render_list(
    title: str,
    items: list[str],
    empty_message: str,
) -> None:
    """
    Render a list of analysis items.
    """

    if not items:
        st.info(empty_message)
        return

    for index, item in enumerate(items, start=1):
        with st.expander(f"{title} {index}", expanded=index == 1):
            st.write(item)