from enum import Enum


class FiscalQuarter(Enum):
    """Represents a fiscal quarter."""

    Q1 = "Q1"
    Q2 = "Q2"
    Q3 = "Q3"
    Q4 = "Q4"

    def __str__(self) -> str:
        return self.value