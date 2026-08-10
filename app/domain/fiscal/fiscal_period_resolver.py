from __future__ import annotations

from datetime import date

from app.domain.documents.document import DocumentType

from .fiscal_quarter import FiscalQuarter
from .resolved_fiscal_period import ResolvedFiscalPeriod


class FiscalPeriodResolver:
    """Resolves fiscal year and fiscal quarter from reporting dates."""

    @staticmethod
    def resolve(
        report_date: date,
        document_type: DocumentType,
        fiscal_year_end_month: int,
        fiscal_year_end_day: int,
    ) -> ResolvedFiscalPeriod:
        """
        Resolve the fiscal reporting period.

        Parameters
        ----------
        report_date
            Period end date reported by the company.

        document_type
            Financial document type.

        fiscal_year_end_month
            Month in which the company's fiscal year ends.

        fiscal_year_end_day
            Day on which the company's fiscal year ends.
        """

        fiscal_year = FiscalPeriodResolver._resolve_fiscal_year(
            report_date=report_date,
            fiscal_year_end_month=fiscal_year_end_month,
            fiscal_year_end_day=fiscal_year_end_day,
        )

        if document_type == DocumentType.TEN_K:
            return ResolvedFiscalPeriod(
                fiscal_year=fiscal_year,
                fiscal_quarter=None,
            )

        quarter = FiscalPeriodResolver._resolve_fiscal_quarter(
            report_date=report_date,
            fiscal_year_end_month=fiscal_year_end_month,
            fiscal_year_end_day=fiscal_year_end_day,
        )

        return ResolvedFiscalPeriod(
            fiscal_year=fiscal_year,
            fiscal_quarter=quarter,
        )

    @staticmethod
    def _resolve_fiscal_year(
        report_date: date,
        fiscal_year_end_month: int,
        fiscal_year_end_day: int,
    ) -> int:
        fiscal_year_end = date(
            report_date.year,
            fiscal_year_end_month,
            fiscal_year_end_day,
        )

        if report_date <= fiscal_year_end:
            return fiscal_year_end.year

        return fiscal_year_end.year + 1

    @staticmethod
    def _resolve_fiscal_quarter(
        report_date: date,
        fiscal_year_end_month: int,
        fiscal_year_end_day: int,
    ) -> FiscalQuarter:
        fiscal_year = FiscalPeriodResolver._resolve_fiscal_year(
            report_date,
            fiscal_year_end_month,
            fiscal_year_end_day,
        )

        previous_year_end = date(
            fiscal_year - 1,
            fiscal_year_end_month,
            fiscal_year_end_day,
        )

        days_elapsed = (report_date - previous_year_end).days

        if days_elapsed <= 92:
            return FiscalQuarter.Q1

        if days_elapsed <= 184:
            return FiscalQuarter.Q2

        if days_elapsed <= 276:
            return FiscalQuarter.Q3

        return FiscalQuarter.Q4