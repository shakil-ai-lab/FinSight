from dataclasses import dataclass

from .fiscal_quarter import FiscalQuarter


@dataclass(frozen=True)
class ResolvedFiscalPeriod:
    """Represents a resolved fiscal reporting period."""

    fiscal_year: int
    fiscal_quarter: FiscalQuarter | None