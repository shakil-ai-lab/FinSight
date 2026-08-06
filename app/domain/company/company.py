from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Company:
    """
    Represents a publicly traded company.
    """

    name: str
    ticker: str
    cik: str