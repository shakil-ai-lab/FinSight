from __future__ import annotations

import streamlit as st

from app.interfaces.streamlit.pages.dashboard import (
    render_dashboard,
)

st.set_page_config(
    page_title="FinSight",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

render_dashboard()