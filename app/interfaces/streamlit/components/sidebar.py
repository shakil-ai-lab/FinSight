from __future__ import annotations

from dataclasses import dataclass

import streamlit as st

from app.application.services.filing_discovery_service import (
    FilingDiscoveryService,
)
from app.domain.analysis import AnalysisRequest, AnalysisType
from app.domain.company import AvailableFilings
from app.domain.documents import FilingMetadata
from app.domain.fiscal import FiscalQuarter


@dataclass(slots=True, frozen=True)
class SidebarResult:
    """
    Result returned by the Streamlit sidebar.
    """

    analysis_request: AnalysisRequest | None
    analyze_clicked: bool


def _format_filing(filing: FilingMetadata) -> str:
    """
    Format a filing for display in the Streamlit selector.
    """

    quarter = (
        f" {filing.fiscal_quarter}"
        if filing.fiscal_quarter is not None
        else ""
    )

    return (
        f"{filing.document_type.value} | "
        f"FY{filing.fiscal_year}{quarter} | "
        f"Filed {filing.filing_date}"
    )


def render_sidebar(
    filing_discovery_service: FilingDiscoveryService,
) -> SidebarResult:
    """
    Render the application sidebar and return the user's selections.
    """

    with st.sidebar:
        st.header("Analysis")

        company_ticker = st.text_input(
            "Company Ticker",
            value="AAPL",
            help="Enter a valid SEC ticker symbol.",
        ).strip().upper()

        load_filings_clicked = st.button(
            "Load SEC Filings",
            use_container_width=True,
        )

        if load_filings_clicked:
            if not company_ticker:
                st.warning("Enter a company ticker first.")
                st.session_state.available_filings = None
            else:
                try:
                    st.session_state.available_filings = (
                        filing_discovery_service.discover(
                            company_ticker,
                        )
                    )
                    st.session_state.selected_filing = None

                except ValueError as exc:
                    st.session_state.available_filings = None
                    st.error(str(exc))

        available_filings: AvailableFilings | None = (
            st.session_state.get("available_filings")
        )

        if available_filings is None:
            st.info("Load SEC filings to select a filing.")

            return SidebarResult(
                analysis_request=None,
                analyze_clicked=False,
            )

        st.caption(
            f"{available_filings.company.name} "
            f"({available_filings.company.ticker})"
        )

        filings = available_filings.filings

        document_types = list(
            dict.fromkeys(
                filing.document_type
                for filing in filings
            )
        )

        filing_type = st.selectbox(
            "Filing Type",
            options=document_types,
            format_func=lambda value: value.value,
        )

        type_filings = [
            filing
            for filing in filings
            if filing.document_type is filing_type
        ]

        fiscal_years = sorted(
            {
                filing.fiscal_year
                for filing in type_filings
            },
            reverse=True,
        )

        fiscal_year = st.selectbox(
            "Fiscal Year",
            options=fiscal_years,
        )

        year_filings = [
            filing
            for filing in type_filings
            if filing.fiscal_year == fiscal_year
        ]

        fiscal_quarter: FiscalQuarter | None = None

        quarter_options = list(
            dict.fromkeys(
                filing.fiscal_quarter
                for filing in year_filings
                if filing.fiscal_quarter is not None
            )
        )

        if quarter_options:
            fiscal_quarter = st.selectbox(
                "Fiscal Quarter",
                options=quarter_options,
                format_func=str,
            )

            selected_filings = [
                filing
                for filing in year_filings
                if filing.fiscal_quarter == fiscal_quarter
            ]
        else:
            selected_filings = year_filings

        selected_filing = st.selectbox(
            "Selected Filing",
            options=selected_filings,
            format_func=_format_filing,
        )

        st.session_state.selected_filing = selected_filing

        st.divider()

        analyze_clicked = st.button(
            "Analyze Company",
            type="primary",
            use_container_width=True,
        )

    analysis_type = (
        AnalysisType.ANNUAL
        if selected_filing.document_type.value == "10-K"
        else AnalysisType.QUARTERLY
    )

    analysis_request = AnalysisRequest(
        company=available_filings.company.name,
        ticker=available_filings.company.ticker,
        analysis_type=analysis_type,
        fiscal_year=selected_filing.fiscal_year,
        fiscal_quarter=selected_filing.fiscal_quarter,
    )

    return SidebarResult(
        analysis_request=analysis_request,
        analyze_clicked=analyze_clicked,
    )