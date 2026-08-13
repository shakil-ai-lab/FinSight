from __future__ import annotations

from bs4 import BeautifulSoup

from app.domain.fiscal import FiscalQuarter


class SECFiscalMetadataParser:
    """
    Extracts authoritative fiscal metadata from an SEC filing.

    SEC Inline XBRL filings expose fiscal metadata through:

    - dei:DocumentFiscalYearFocus
    - dei:DocumentFiscalPeriodFocus

    This parser is responsible only for extracting those values.
    It does not perform fiscal-period inference.
    """

    _FISCAL_YEAR_TAG = "documentfiscalyearfocus"
    _FISCAL_PERIOD_TAG = "documentfiscalperiodfocus"

    def parse(self, html: str) -> tuple[int, FiscalQuarter | None]:
        """
        Extract fiscal year and fiscal quarter from SEC filing HTML.

        Parameters
        ----------
        html:
            Raw SEC filing HTML.

        Returns
        -------
        tuple[int, FiscalQuarter | None]
            Fiscal year and fiscal quarter.

            For 10-Q:
                (2024, FiscalQuarter.Q3)

            For 10-K:
                (2024, None)

        Raises
        ------
        ValueError
            If fiscal year metadata is missing or invalid.
        """

        soup = BeautifulSoup(html, "html.parser")

        fiscal_year_text = self._find_text(
            soup,
            self._FISCAL_YEAR_TAG,
        )

        if fiscal_year_text is None:
            raise ValueError(
                "SEC filing is missing "
                "DocumentFiscalYearFocus metadata."
            )

        try:
            fiscal_year = int(fiscal_year_text)
        except ValueError as exc:
            raise ValueError(
                "SEC filing contains an invalid "
                "DocumentFiscalYearFocus value: "
                f"{fiscal_year_text!r}"
            ) from exc

        fiscal_period_text = self._find_text(
            soup,
            self._FISCAL_PERIOD_TAG,
        )

        if fiscal_period_text is None:
            raise ValueError(
                "SEC filing is missing "
                "DocumentFiscalPeriodFocus metadata."
            )

        fiscal_quarter = self._resolve_fiscal_quarter(
            fiscal_period_text
        )

        return fiscal_year, fiscal_quarter

    @staticmethod
    def _find_text(
        soup: BeautifulSoup,
        tag_name: str,
    ) -> str | None:
        """
        Find an XBRL fiscal metadata element by local tag name.

        SEC filings may represent the tag with namespace
        prefixes such as:

            dei:DocumentFiscalYearFocus

        BeautifulSoup may expose the tag name differently depending
        on the HTML/XML structure, so matching is performed using
        the final local tag name.
        """

        for tag in soup.find_all():
            local_name = tag.name.split(":")[-1].lower()

            if local_name == tag_name:
                text = tag.get_text(strip=True)

                if text:
                    return text

        return None

    @staticmethod
    def _resolve_fiscal_quarter(
        fiscal_period: str,
    ) -> FiscalQuarter | None:
        """
        Convert SEC fiscal-period metadata into the domain enum.

        Q1/Q2/Q3/Q4 represent quarterly filings.

        FY represents the annual fiscal period used by 10-K,
        therefore the domain quarter is None.
        """

        normalized = fiscal_period.strip().upper()

        quarter_mapping = {
            "Q1": FiscalQuarter.Q1,
            "Q2": FiscalQuarter.Q2,
            "Q3": FiscalQuarter.Q3,
            "Q4": FiscalQuarter.Q4,
        }

        if normalized in quarter_mapping:
            return quarter_mapping[normalized]

        if normalized in {"FY", "FY0", "ANNUAL"}:
            return None

        raise ValueError(
            "SEC filing contains an unsupported "
            "DocumentFiscalPeriodFocus value: "
            f"{fiscal_period!r}"
        )