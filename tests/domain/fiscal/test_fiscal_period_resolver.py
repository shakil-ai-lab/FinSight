from datetime import date

from app.domain.documents.document_type import DocumentType
from app.domain.fiscal import (
    FiscalQuarter,
)
from app.domain.fiscal.fiscal_period_resolver import FiscalPeriodResolver


class TestFiscalPeriodResolver:

    def test_resolve_december_year_end_q1(self):
        period = FiscalPeriodResolver.resolve(
            report_date=date(2025, 3, 31),
            document_type=DocumentType.TEN_Q,
            fiscal_year_end_month=12,
            fiscal_year_end_day=31,
        )

        assert period.fiscal_year == 2025
        assert period.fiscal_quarter == FiscalQuarter.Q1

    def test_resolve_december_year_end_q2(self):
        period = FiscalPeriodResolver.resolve(
            report_date=date(2025, 6, 30),
            document_type=DocumentType.TEN_Q,
            fiscal_year_end_month=12,
            fiscal_year_end_day=31,
        )

        assert period.fiscal_year == 2025
        assert period.fiscal_quarter == FiscalQuarter.Q2

    def test_resolve_december_year_end_q3(self):
        period = FiscalPeriodResolver.resolve(
            report_date=date(2025, 9, 30),
            document_type=DocumentType.TEN_Q,
            fiscal_year_end_month=12,
            fiscal_year_end_day=31,
        )

        assert period.fiscal_year == 2025
        assert period.fiscal_quarter == FiscalQuarter.Q3

    def test_resolve_december_year_end_q4(self):
        period = FiscalPeriodResolver.resolve(
            report_date=date(2025, 12, 31),
            document_type=DocumentType.TEN_Q,
            fiscal_year_end_month=12,
            fiscal_year_end_day=31,
        )

        assert period.fiscal_year == 2025
        assert period.fiscal_quarter == FiscalQuarter.Q4

    def test_resolve_annual_filing(self):
        period = FiscalPeriodResolver.resolve(
            report_date=date(2025, 12, 31),
            document_type=DocumentType.TEN_K,
            fiscal_year_end_month=12,
            fiscal_year_end_day=31,
        )

        assert period.fiscal_year == 2025
        assert period.fiscal_quarter is None

    def test_resolve_june_year_end_q1(self):
        period = FiscalPeriodResolver.resolve(
            report_date=date(2024, 9, 30),
            document_type=DocumentType.TEN_Q,
            fiscal_year_end_month=6,
            fiscal_year_end_day=30,
        )

        assert period.fiscal_year == 2025
        assert period.fiscal_quarter == FiscalQuarter.Q1

    def test_resolve_june_year_end_q2(self):
        period = FiscalPeriodResolver.resolve(
            report_date=date(2024, 12, 31),
            document_type=DocumentType.TEN_Q,
            fiscal_year_end_month=6,
            fiscal_year_end_day=30,
        )

        assert period.fiscal_year == 2025
        assert period.fiscal_quarter == FiscalQuarter.Q2

    def test_resolve_june_year_end_q3(self):
        period = FiscalPeriodResolver.resolve(
            report_date=date(2025, 3, 31),
            document_type=DocumentType.TEN_Q,
            fiscal_year_end_month=6,
            fiscal_year_end_day=30,
        )

        assert period.fiscal_year == 2025
        assert period.fiscal_quarter == FiscalQuarter.Q3

    def test_resolve_june_year_end_q4(self):
        period = FiscalPeriodResolver.resolve(
            report_date=date(2025, 6, 30),
            document_type=DocumentType.TEN_Q,
            fiscal_year_end_month=6,
            fiscal_year_end_day=30,
        )

        assert period.fiscal_year == 2025
        assert period.fiscal_quarter == FiscalQuarter.Q4

    def test_boundary_day_before_fiscal_year_end(self):
        period = FiscalPeriodResolver.resolve(
            report_date=date(2025, 6, 29),
            document_type=DocumentType.TEN_Q,
            fiscal_year_end_month=6,
            fiscal_year_end_day=30,
        )

        assert period.fiscal_year == 2025

    def test_boundary_day_after_fiscal_year_end(self):
        period = FiscalPeriodResolver.resolve(
            report_date=date(2025, 7, 1),
            document_type=DocumentType.TEN_Q,
            fiscal_year_end_month=6,
            fiscal_year_end_day=30,
        )

        assert period.fiscal_year == 2026


    def test_apple_q1_from_real_sec_filing(self):
        """
        Apple Form 10-Q:
        Fiscal quarter ended December 28, 2024.

        Apple's FY2024 ended September 28, 2024.
        Therefore December 28, 2024 belongs to FY2025 Q1.
        """
        period = FiscalPeriodResolver.resolve(
            report_date=date(2024, 12, 28),
            document_type=DocumentType.TEN_Q,
            fiscal_year_end_month=9,
            fiscal_year_end_day=28,
        )

        assert period.fiscal_year == 2025
        assert period.fiscal_quarter == FiscalQuarter.Q1

    def test_microsoft_q1_from_real_sec_filing(self):
        """
        Microsoft Form 10-Q:
        Fiscal quarter ended September 30, 2025.

        Microsoft's fiscal year ends June 30.
        Therefore September 30, 2025 belongs to FY2026 Q1.
        """
        period = FiscalPeriodResolver.resolve(
            report_date=date(2025, 9, 30),
            document_type=DocumentType.TEN_Q,
            fiscal_year_end_month=6,
            fiscal_year_end_day=30,
        )

        assert period.fiscal_year == 2026
        assert period.fiscal_quarter == FiscalQuarter.Q1

    def test_tesla_q1_from_real_sec_filing(self):
        """
        Tesla Form 10-Q:
        Fiscal quarter ended March 31, 2025.

        Tesla's fiscal year ends December 31.
        Therefore March 31, 2025 belongs to FY2025 Q1.
        """
        period = FiscalPeriodResolver.resolve(
            report_date=date(2025, 3, 31),
            document_type=DocumentType.TEN_Q,
            fiscal_year_end_month=12,
            fiscal_year_end_day=31,
        )

        assert period.fiscal_year == 2025
        assert period.fiscal_quarter == FiscalQuarter.Q1

    def test_nvidia_q1_from_real_sec_filing(self):
        """
        NVIDIA Form 10-Q:
        Fiscal quarter ended April 27, 2025.

        NVIDIA's FY2025 ended January 26, 2025.
        Therefore April 27, 2025 belongs to FY2026 Q1.
        """
        period = FiscalPeriodResolver.resolve(
            report_date=date(2025, 4, 27),
            document_type=DocumentType.TEN_Q,
            fiscal_year_end_month=1,
            fiscal_year_end_day=26,
        )

        assert period.fiscal_year == 2026
        assert period.fiscal_quarter == FiscalQuarter.Q1    