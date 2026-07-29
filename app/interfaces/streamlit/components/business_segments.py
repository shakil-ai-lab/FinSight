from __future__ import annotations

from dataclasses import dataclass

import streamlit as st


@dataclass(slots=True, frozen=True)
class BusinessSegmentView:
    """
    Presentation model for a business segment.
    """

    name: str
    revenue: str
    growth: str


def render_business_segments(
    segments: list[BusinessSegmentView],
) -> None:
    """
    Render business segment performance.
    """

    with st.container(border=True):

        st.subheader("🌍 Business Segments")

        if not segments:
            st.info("No business segment information available.")
            return

        header = st.columns([3, 2, 1])

        header[0].markdown("**Segment**")
        header[1].markdown("**Revenue**")
        header[2].markdown("**Growth**")

        st.divider()

        for segment in segments:

            col1, col2, col3 = st.columns([3, 2, 1])

            col1.write(segment.name)
            col2.write(segment.revenue)

            growth = segment.growth.strip()

            if growth.startswith("-"):
                col3.error(growth)

            elif growth.startswith("+"):
                col3.success(growth)

            else:
                col3.info(growth)