from __future__ import annotations

import streamlit as st


def render_executive_summary(summary: str) -> None:
    """
    Render the AI-generated executive summary.
    """

    with st.container(border=True):
        st.subheader("📝 Executive Summary")

        st.write(summary)