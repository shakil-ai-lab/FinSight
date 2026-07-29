from __future__ import annotations

import streamlit as st


def render_header() -> None:
    """
    Render the application header.

    This component is responsible only for displaying the
    FinSight branding and page title.
    """

    st.title("📊 FinSight")

    st.caption(
        "AI-Powered Financial Statement Analysis & Investment Decision Support"
    )

    st.divider()